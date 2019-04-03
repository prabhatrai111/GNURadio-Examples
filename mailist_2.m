%link for SDR config for LTE transmission and reception.
%https://www.mathworks.com/help/supportpkg/xilinxzynqbasedradio/examples/transmit-and-receive-lte-mimo-using-a-single-analog-devices-ad9361-ad9364.html
%%
% Check that LTE System Toolbox is installed, and that there is a valid license
if isempty(ver('lte')) % Check for LST install
    error('zynqRadioLTEMIMOTransmitReceive:NoLST', ...
        'Please install LTE System Toolbox to run this example.');
elseif ~license('test', 'LTE_Toolbox') % Check that a valid license is present
    error('zynqRadioLTEMIMOTransmitReceive:NoLST', ...
        'A valid license for LTE System Toolbox is required to run this example.');
end

%% Setup handle for image plot
if ~exist('imFig', 'var') || ~ishandle(imFig)
    imFig = figure;
    imFig.NumberTitle = 'off';
    imFig.Name = 'Image Plot';
    imFig.Visible = 'off';
else   
    clf(imFig); % Clear figure
    imFig.Visible = 'off';
end

% Setup handle for channel estimate plots
if ~exist('hhest', 'var') || ~ishandle(hhest)
    hhest = figure('Visible','Off');
    hhest.NumberTitle = 'off';
    hhest.Name = 'Channel Estimate';
else
    clf(hhest); % Clear figure
    hhest.Visible = 'off';
end

% Setup Spectrum viewer
spectrumScope = dsp.SpectrumAnalyzer( ...
    'SpectrumType',    'Power density', ...
    'SpectralAverages', 10, ...
    'YLimits',         [-150 -60], ...
    'Title',           'Received Baseband LTE Signal Spectrum', ...
    'YLabel',          'Power spectral density');

%%  Initialize SDR device
tx = struct; % Create empty structure for transmitter
tx.SDRDeviceName = 'ZedBoard and FMCOMMS2/3/4'; % Set SDR Device
radio = sdrdev(tx.SDRDeviceName); % Create SDR device object
% Connect to the SDR device, and get device info
devInfo = radio.info;

%% Creating the Measurement Report Struct
req = struct();
req.getPBCH= [];   % to obtain PBCH Information
req.getPMCH= [];   % to obtain PMCH Information
req.getPCFICH= []; % to obtain PCFICH Information
req.getPDCCH= [];  % to obtain PDCCH Information
req.getPDSCH= [];  % to obtain PDSCH Information


%% Creating the Transmitter for the eNB
%Bandwidth (NDLRB) must be greater than or equal to allocations
tx.RC = 'R.7';                         % Base RMC Configuration.
tx.NDLRB = 50;                         % Set the bandwidth
tx.TotFrames = 1;                      % Number of frames to generate
tx.NTxAnts = 1;                        % Number of Transmit Antennas
tx.NCellID = 88;                       % CellID
tx.NFrame =  700;                      % Initial Frame Number.
BandNoLUT = [1 2 3 4 5 7 8 10 12 13 14 17 18 19 20 25 ...
     26 27 28 29]; % Band Number Lookup Table
CenterFreqLUT =[2100 1900 1800 1700 850 2600 900 1700 ...
    700 700 700 700 850 850 800 1900 850 800 ...
    700 700]*1e6;  % Center Frequency Lookup Table
SampleRateLUT = [1.92 3.84 7.68 15.36 30.72]*1e6;
ChannelBandwidthLUT = [1.4 3 5 10 15];
prompt ='Hello User, please enter a band from the list:1 2 3 4 5 7 8 10 12 13 14 17 18 19 20 25 26 27 28 29. \n';
BandNo = input(prompt);
tx.DesiredCenterFrequency = CenterFreqLUT(BandNoLUT==BandNo); % Center Frequency for Selected Band
if isempty(tx.DesiredCenterFrequency)
    error('E-UTRA Band not supported. Supported E-UTRA bands are.%s \n',...
            '1 2 3 4 5 7 8 10 12 13 14 17 18 19 20 25 26 27 28 29');
end
prompt1 ='Hello User, please enter a channel bandwidth from the list: 1.4MHz 3MHz 5MHz 10MHz 15MHz \n';
SamplingRate = input(prompt1);
tx.RadioFrontEndSampleRate = SampleRateLUT(ChannelBandwidthLUT==SamplingRate); % Sampling Rate for Selected Band
if isempty(tx.RadioFrontEndSampleRate)
    error('Bandwidth Channel not supported. Supported Channel Bandwidths are: %s \n',...
            '1.4 MHz, 3 MHz, 5 MHz, 10 MHz, 15 MHz');
end

% If using an FMCOMMS4, set number of TX antennas to 1 as there is only one
% channel available... 
if ~isempty(strfind(devInfo.RFBoardVersion, 'AD-FMCOMMS4-EBZ')) && (tx.NTxAnts ~= 1)
    fprintf('\nFMCOMMS4 detected: Changing number of transmit antennas to 1.\n');
    tx.NTxAnts = 1;
end

% TX gain parameter: 
% Change this parameter to reduce transmission quality, and impair the
% signal. Suggested values:
%    * set to -10 for default gain (-10dB)
%    * set to -20 for reduced gain (-20dB)
%
% NOTE: These are suggested values -- depending on your antenna
% configuration, you may have to tweak these values.
tx.Gain = -10;

%% Preparation of File to be sent Across System.
data = 'peppers.png';            % Image file name
fData = imread(data);            % Read image data from file
scale = 0.5;                       % Image scaling factor
origSize = size(fData);            % Original input image size
scaledSize = max(floor(scale.*origSize(1:2)),1); % Calculate new image size
heightIx = min(round(((1:scaledSize(1))-0.5)./scale+0.5),origSize(1));
widthIx = min(round(((1:scaledSize(2))-0.5)./scale+0.5),origSize(2));
fData = fData(heightIx,widthIx,:); % Resize image
imsize = size(fData);              % Store new image size
binData = dec2bin(fData(:),8);     % Convert to 8 bit unsigned binary
trData = reshape((binData-'0').',1,[]).'; % Create binary stream
%% Random generation of sampling criteria

a= randi([1,8]);                                   % PBCH minimum index value
b= randi([8,16]);                                  % PBCH maximum index value
a1= randi([1,480]);                                % PDCCH minimum index value for subframe 
b1= randi([480,960]);                              % PDCCH maximum index value for subframe
c1 = randi([1,10]);                                % Subframe which is being sampled for PDCCH
a2= randi([1,3450]);                               % PDSCH minimum index value for subframe
b2= randi([3450,6900]);                            % PDSCH maximum index value for subframe
c2 = randi([2,8]);                                 % Subframe which is being sampled for PDSCH
a_bin = dec2bin(a,8);                              % Converting the index value to a 8 bit binary char
a_bin_stream = reshape((a_bin-'0').',1,[]).';      % Converting the 8 bit binary char to a binary stream
b_bin = dec2bin(b,8);                              % Process repeated for other indices
b_bin_stream = reshape((b_bin-'0').',1,[]).';
a1_bin = dec2bin(a1,8);
a1_bin_stream = reshape((a1_bin-'0').',1,[]).';
b1_bin = dec2bin(b1,8);
b1_bin_stream = reshape((b1_bin-'0').',1,[]).';
c1_bin = dec2bin(c1,8);
c1_bin_stream = reshape((c1_bin-'0').',1,[]).';
a2_bin = dec2bin(a2,8);
a2_bin_stream = reshape((a2_bin-'0').',1,[]).';
b2_bin = dec2bin(b2,8);
b2_bin_stream = reshape((b2_bin-'0').',1,[]).';
c2_bin = dec2bin(c2,8);
c2_bin_stream = reshape((c2_bin-'0').',1,[]).';

% Compiling all the binary data streams.
dataStream = [trData;a_bin_stream;b_bin_stream;a1_bin_stream;...
    b1_bin_stream;c1_bin_stream;a2_bin_stream ;b2_bin_stream;...
    c2_bin_stream]; 
%% Plot transmit image
figure(1)
subplot(211);
    imshow(fData);
    title('Transmitted Image');
subplot(212);
    title('Received image will appear here...');
    set(gca,'Visible','off'); % Hide axes
    set(findall(gca, 'type', 'text'), 'visible', 'on'); % Unhide title
    
pause(1); % Pause to plot Tx image

%% Create RMC 

DLRMC  = lteRMCDL(tx.RC);           % Create the full RMC. 


% Calculate the required number of LTE frames based on the size of the
% image data
trBlkSize = DLRMC.PDSCH.TrBlkSizes;
tx.TotFrames = ceil(numel(dataStream)/sum(trBlkSize(:)));

% Customize RMC parameters
DLRMC.NCellID = tx.NCellID;
DLRMC.NFrame = tx.NFrame;
DLRMC.TotSubframes = tx.TotFrames*10; % 10 subframes per frame
DLRMC.CellRefP = tx.NTxAnts; % Configure number of cell reference ports
DLRMC.PDSCH.RVSeq = 0;

% Fill subframe 5 with dummy data
DLRMC.OCNGPDSCHEnable = 'On';
DLRMC.OCNGPDCCHEnable = 'On';

fprintf('\nGenerating LTE transmit waveform:\n')
fprintf('  Packing image data into %d frame(s).\n\n', ...
    tx.TotFrames);

% Pack the Image Data and request values into a single LTE Frame. 
[eNodeBOutput,txGrid,DLRMC] = lteRMCDLTool(DLRMC,dataStream);

%% Prepare for Transmission.
sdrTransmitter = sdrtx(tx.SDRDeviceName);
sdrTransmitter.BasebandSampleRate = tx.RadioFrontEndSampleRate; 
% 15.36 Msps for default RMC (R.7)
% with a bandwidth of 10 MHz
sdrTransmitter.CenterFrequency = tx.DesiredCenterFrequency;
sdrTransmitter.ShowAdvancedProperties = true;
sdrTransmitter.BypassUserLogic = true;
sdrTransmitter.Gain = tx.Gain;

% Apply TX channel mapping
if tx.NTxAnts == 2
    fprintf('Setting channel map to ''[1 2]''.\n\n');
    sdrTransmitter.ChannelMapping = [1,2];
else
    fprintf('Setting channel map to ''1''.\n\n');
    sdrTransmitter.ChannelMapping = 1;
end
% Scale the signal for better power output.
powerScaleFactor = 0.8;
eNodeBOutput = eNodeBOutput.*(1/max(abs(eNodeBOutput))*powerScaleFactor);


% Cast the transmit signal to int16 ---
% this is the native format for the SDR hardware.
eNodeBOutput = int16(eNodeBOutput*2^15);

% The |transmitRepeat| function transfers the baseband LTE transmission to
% the SDR platform, and stores the signal samples in hardware memory. The
% example then transmits the waveform continuously over the air without
% gaps until the release method for the transmit object is released.
% Messages are displayed in the command window to confirm that transmission
% has started successfully.
transmitRepeat(sdrTransmitter, eNodeBOutput);

%%
% User defined parameters --- configure the same as transmitter
rxsim = struct;
rxsim.RadioFrontEndSampleRate = sdrTransmitter.BasebandSampleRate; % Configure for same sample rate
                                                       % as transmitter
rxsim.RadioCenterFrequency = sdrTransmitter.CenterFrequency;
rxsim.NRxAnts = tx.NTxAnts;
rxsim.FramesPerBurst = tx.TotFrames+1; % Number of LTE frames to capture in each burst.
                                          % Capture 1 more LTE frame than transmitted to
                                          % allow for timing offset wraparound...
rxsim.numBurstCaptures = 1; % Number of bursts to capture

% Derived parameters
samplesPerFrame = 10e-3*rxsim.RadioFrontEndSampleRate; % LTE frames period is 10 ms

rxsim.SDRDeviceName = tx.SDRDeviceName;

sdrReceiver = sdrrx(rxsim.SDRDeviceName);
sdrReceiver.BasebandSampleRate = rxsim.RadioFrontEndSampleRate;
sdrReceiver.CenterFrequency = rxsim.RadioCenterFrequency;
sdrReceiver.SamplesPerFrame = samplesPerFrame;
sdrReceiver.OutputDataType = 'double';
sdrReceiver.EnableBurstMode = true;
sdrReceiver.NumFramesInBurst = rxsim.FramesPerBurst;

% Configure RX channel map
if rxsim.NRxAnts == 2
    sdrReceiver.ChannelMapping = [1,2];
else
    sdrReceiver.ChannelMapping = 1;
end
% burstCaptures holds sdrReceiver.FramesPerBurst number of consecutive frames worth
% of baseband LTE samples. Each column holds one LTE frame worth of data.
burstCaptures = zeros(samplesPerFrame,rxsim.NRxAnts,rxsim.FramesPerBurst);

%% Receiver for Downlink.
% *LTE Receiver Setup* 

enb.PDSCH = DLRMC.PDSCH;
enb.DuplexMode = 'FDD';
enb.CyclicPrefix = 'Normal';
enb.CellRefP = 1;

% Bandwidth: {1.4 MHz, 3 MHz, 5 MHz, 10 MHz, 20 MHz}
SampleRateLUT = [1.92 3.84 7.68 15.36 30.72]*1e6;
NDLRBLUT = [6 15 25 50 100];
enb.NDLRB = NDLRBLUT(SampleRateLUT==rxsim.RadioFrontEndSampleRate);
if isempty(enb.NDLRB)
    error('Sampling rate not supported. Supported rates are %s.',...
            '1.92 MHz, 3.84 MHz, 7.68 MHz, 15.36 MHz, 30.72 MHz');
end
fprintf('\nSDR hardware sampling rate configured to capture %d LTE RBs.\n',enb.NDLRB);

%% Channel estimation configuration structure

cec.PilotAverage = 'UserDefined';  % Type of pilot symbol averaging
cec.FreqWindow = 9;                % Frequency window size in REs
cec.TimeWindow = 9;                % Time window size in REs
cec.InterpType = 'Cubic';          % 2D interpolation type
cec.InterpWindow = 'Centered';     % Interpolation window type
cec.InterpWinSize = 3;             % Interpolation window size


%% *Signal Capture and Processing*

% This uses a while loop to capture and decode bursts of LTE Frames. 
% As the LTE waveform is continually transmitted over the air in a loop,
% the first frame that is captured by the receiver is not guaranteed to be
% the first frame that was transmitted. This means that the frames may be
% decoded in out of sequence. The frame numbers therefore, are required.The
% Master Information Block(MIB) contains information on the current system
% frame number and therefore must be decoded. After the frame number is
% known, then can the PDSCH and DLSCH can be decoded. No data is 
% transmitted in subframe 5; therefore the captured data for subframe 
% is ignored for the decoding. The Power Spectral Density (PSD) of the 
% captured waveform is plotted to show the received LTE transmission. 
% When the LTE frames have been successfully decoded, the detected frame
% number is displayed in the command window on a frame-by-frame basis, and
% the equalized PDSCH symbol constellation is shown for each subframe. An
% estimate of the channel magnitude frequency response between cell
% reference point 0 and the receive antennae is also shown for each frame.

enbDefault = enb;

while rxsim.numBurstCaptures

    % Set default LTE parameters
    enb = enbDefault;

    % SDR Capture
    fprintf('\nStarting a new RF capture.\n\n')
    len = 0;
    for frame = 1:rxsim.FramesPerBurst
        while len == 0
            % Store one LTE frame worth of samples
            [data,len,lostSamples] = sdrReceiver();
            burstCaptures(:,:,frame) = data;
        end
        if lostSamples
            warning('Dropped samples');
        end
        len = 0;
    end
    rxWaveform = burstCaptures(:);
    spectrumScope.SampleRate = rxsim.RadioFrontEndSampleRate;
    spectrumScope(rxWaveform);

    %% Perform frequency offset correction for known cell ID
    frequencyOffset = lteFrequencyOffset(enb,rxWaveform);
    rxWaveform = lteFrequencyCorrect(enb,rxWaveform,frequencyOffset);
    fprintf('\nCorrected a frequency offset of %i Hz.\n',frequencyOffset)
    
    %% Perform the blind cell search to obtain cell identity and timing offset
    %   Use 'PostFFT' SSS detection method to improve speed
    cellSearch.SSSDetection = 'PostFFT'; cellSearch.MaxCellCount = 1;
    [NCellID,frameOffset] = lteCellSearch(enb,rxWaveform,cellSearch);
    fprintf('Detected a cell identity of %i.\n', NCellID);
    enb.NCellID = NCellID; % From lteCellSearch
    
    %% Sync the captured samples to the start of an LTE frame, and trim off
    % any samples that are part of an incomplete frame.
    rxWaveform = rxWaveform(frameOffset+1:end,:);
    tailSamples = mod(length(rxWaveform),samplesPerFrame);
    rxWaveform = rxWaveform(1:end-tailSamples,:);
    enb.NSubframe = 0;
    fprintf('Corrected a timing offset of %i samples.\n',frameOffset)    
    
    %% Perform OFDM Demodulation
    rxGrid = lteOFDMDemodulate(enb,rxWaveform);
    % Estimate the channel on the middle 6 RBs 
    [hest, nest] = lteDLChannelEstimate(enb,cec,rxGrid);
    % Extract resource elements corresponding to the PBCH from the first
    % subframe across all receive antennas and channel estimates
    sfDims = lteResourceGridSize(enb); 
    Lsf = sfDims(2); %OFDM Symbols per subframe
    LFrame = 10*Lsf; %OFDM Symbols per Frame
    numFullFrames = floor(length(rxWaveform)/samplesPerFrame);
    enb.NSubframe = 0;
    rxDataFrame = zeros(sum(enb.PDSCH.TrBlkSizes(:)),numFullFrames);
    recFrames = zeros(numFullFrames,1);
    rxSymbols = []; 
    txSymbols = [];
    pcfichindex= [];
    
    %% Decoding the Information Received. 
    for frame = 0:(numFullFrames-1)
        fprintf('\nPerforming DL-SCH Decode for frame %i of %i in burst:\n', ...
            frame+1,numFullFrames)
        enb.NSubframe = 0;
        rxsf = rxGrid(:,frame*LFrame+(1:Lsf),:);
        hestsf = hest(:,frame*LFrame+(1:Lsf),:,:); 
        
        enb.CellRefP = 1;
        pbchIndices = ltePBCHIndices(enb);
        [pbchRx,pbchHest] = lteExtractResources(pbchIndices,rxsf,hestsf);
        [~,~,nfmod4,mib,CellRefP] = ltePBCHDecode(enb,pbchRx,pbchHest,nest);
           req.getPBCH(:,frame+1)= pbchRx;

        % If PBCH decoding successful CellRefP~=0 then update info
        if ~CellRefP
            fprintf('  No PBCH detected for frame.\n');
            continue;
        end
        enb.CellRefP = CellRefP; % From ltePBCHDecode
    %% Parse MIB bits
        enb = lteMIB(mib,enb);
        enb.NFrame = enb.NFrame+nfmod4;
        recFrames(frame+1)= enb.NFrame;
        fprintf('  Successful MIB Decode.\n')
        fprintf('  Frame number: %d.\n',enb.NFrame);
        
        % The eNodeB transmission bandwidth may be greater than the
        % captured bandwidth, so limit the bandwidth for processing   
        
        enb.NDLRB = min(enbDefault.NDLRB,enb.NDLRB);
        
        % Store received frame number
        recFrames(frame+1) = enb.NFrame;       
        
        for sf=0:9
            if sf~=5
                enb.NSubframe = sf;
                rxsf = rxGrid(:,frame*LFrame+sf*Lsf+(1:Lsf),:);
                % Perform channel estimation with the correct number of CellRefP
                [hestsf,nestsf] = lteDLChannelEstimate(enb,cec,rxsf);
    %% Decode PCFICH
 % PCFICH demodulation. Extract REs corresponding to the PCFICH
                % from the received grid and channel estimate for demodulation.
                pcfichIndices = ltePCFICHIndices(enb);
                pcfichindex{sf+1} = pcfichIndices;
                [pcfichRx,pcfichHest] = lteExtractResources(pcfichIndices,rxsf,hestsf);
                req.getPCFICH(:,sf+1) = pcfichRx;
                
                % CFI decoding             
                [cfiBits,recsym] = ltePCFICHDecode(enb,pcfichRx,pcfichHest,nestsf);
                enb.CFI = lteCFIDecode(cfiBits);        % Get CFI
   
    %% PDCCH demodulation. The PDCCH is now demodulated and decoded using
    % similar resource extraction and decode functions to those shown
    % already for BCH and CFI reception

                pdcchIndices = ltePDCCHIndices(enb); % Get PDCCH indices
                pdcchindex{sf+1} = pdcchIndices;
                [pdcchRx, pdcchHest] = lteExtractResources(pdcchIndices, rxsf,hestsf);
                req.getPDCCH(:,sf+1) = pdcchRx;
    %% Decode PDCCH
                [dciBits, pdcchSymbols] = ltePDCCHDecode(enb, pdcchRx, pdcchHest, nestsf);

    % PDCCH blind search for System Information (SI) and DCI decoding. The
    % LTE System Toolbox provides full blind search of the PDCCH to find
    % any DCI messages with a specified RNTI, in this case the SI-RNTI.
                pdcch = struct('RNTI', 65535);  
                DCI = ltePDCCHSearch(enb, pdcch, dciBits); % Search PDCCH for DCI

                enb.CFI = lteCFIDecode(cfiBits);
                [pdschIndices,pdschIndicesInfo] = ltePDSCHIndices(enb, enb.PDSCH, enb.PDSCH.PRBSet); 
                pdschindex{sf+1} = pdschIndices;
                [pdschRx, pdschHest] = lteExtractResources(pdschIndices, rxsf, hestsf); 
                 req.getPDSCH{sf+1} = pdschRx; 
    %% Decode PDSCH 
                [dlschBits,rxsyms] = ltePDSCHDecode(enb, enb.PDSCH, pdschRx, pdschHest, nestsf); 
                 rxSymbols = [rxSymbols;rxsyms{:}];
                outLen = enb.PDSCH.TrBlkSizes(enb.NSubframe+1);
    %% Decode DL-SCH 
                 [decbits{sf+1}, blkcrc(sf+1)] = lteDLSCHDecode(enb,enb.PDSCH,...
                                                    outLen, dlschBits); 

%% Recode transmitted PDSCH symbols for EVM calculation                            
                %   Encode transmitted DLSCH 
                txRecode = lteDLSCH(enb,enb.PDSCH,pdschIndicesInfo.G,decbits{sf+1});
                %   Modulate transmitted PDSCH
                txRemod = ltePDSCH(enb, enb.PDSCH, txRecode);
                %   Decode transmitted PDSCH
                [~,refSymbols] = ltePDSCHDecode(enb, enb.PDSCH, txRemod);
                %   Add encoded symbol to stream
                txSymbols = [txSymbols; refSymbols{:}]; %#ok<AGROW>

            end
        end
            % Reassemble decoded bits
            fprintf('  Retrieving decoded transport block data.\n');
            rxdata = [];
            for i = 1:length(decbits)
                if i~=6 % Ignore subframe 5
                    rxdata = [rxdata; decbits{i}{:}]; %#ok<AGROW>
                end
            end

            % Store data from receive frame
            rxDataFrame(:,frame+1) = rxdata;
            
    end
    rxsim.numBurstCaptures = rxsim.numBurstCaptures-1;
end
% Release both transmit and receive objects once reception is complete
release(sdrTransmitter);
release(sdrReceiver);
%%
% Recombine received data blocks (in correct order) into continuous stream
[~,frameIdx] = min(recFrames);
fprintf('\nRecombining received data blocks:\n');
    decodedRxDataStream = zeros(length(rxDataFrame(:)),1);
    frameLen = size(rxDataFrame,1);
    
for n=1:numFullFrames
    currFrame = mod(frameIdx-1,numFullFrames)+1; % Get current frame index
    decodedRxDataStream((n-1)*frameLen+1:n*frameLen) = rxDataFrame(:,currFrame);
    frameIdx = frameIdx+1; % Increment frame index
end

% Recreate image from received data
%%
c10 = length(trData);
c11 = length(a_bin_stream);
c12 = length(b_bin_stream);
c13 = length(a1_bin_stream);
c14 = length(b1_bin_stream);
c15 = length(c1_bin_stream);
c16 = length(a2_bin_stream);
c17 = length(b2_bin_stream);
c18 = length(c2_bin_stream);
%%
% Recreate image from received data

str1 = reshape(sprintf('%d',decodedRxDataStream(1:c10)).',8,[]).';
str2 = reshape(sprintf('%d',decodedRxDataStream((1+c10):(c10+c11))).',c11,[]).';
str3 = reshape(sprintf('%d',decodedRxDataStream((c10+c11+1):(c10+c11+c12))).',c12,[]).';
str4 = reshape(sprintf('%d',decodedRxDataStream((c10+c11+c12+1):(c10+c11+c12+c13))).',c13,[]).';
str5 = reshape(sprintf('%d',decodedRxDataStream((c10+c11+c12+c13+1):(c10+c11+c12+c13+c14))).',c14,[]).';
str6 = reshape(sprintf('%d',decodedRxDataStream((c10+c11+c12+c13+c14+1):(c15+c10+c11+c12+c13+c14))).',c15,[]).';
str7 = reshape(sprintf('%d',decodedRxDataStream((c10+c11+c12+c13+c14+c15+1):(c16+c10+c11+c12+c13+c14+c15))).',c16,[]).';
str8 = reshape(sprintf('%d',decodedRxDataStream((c10+c11+c12+c13+c14+c15+c16+1):(c17+c10+c11+c12+c13+c14+c15+c16))).',c17,[]).';
str9 = reshape(sprintf('%d',decodedRxDataStream((c10+c11+c12+c13+c14+c15+c16+c17+1):length(dataStream))).',c18,[]).';
decdata = uint8(bin2dec(str1));
decdata1 = uint8(bin2dec(str2));
decdata2 = (bin2dec(str3));
decdata3 = (bin2dec(str4));
decdata4 = (bin2dec(str5));
decdata5 = uint8(bin2dec(str6));
decdata6 = (bin2dec(str7));
decdata7 = (bin2dec(str8));
decdata8 = uint8(bin2dec(str9));
fprintf('\nConstructing image from received data.\n');
receivedImage = reshape(decdata,imsize);
% Plot receive image
% Plot receive image
if exist('imFig', 'var') && ishandle(imFig) % If TX figure is open
    figure(imFig); subplot(212);
else
    figure; subplot(212);
end
imshow(receivedImage);
title(sprintf('Received Image: %dx%d Antenna Configuration',tx.NTxAnts, rxsim.NRxAnts));