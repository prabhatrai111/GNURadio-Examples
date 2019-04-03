% Setup Spectrum viewer
spectrumScope1 = dsp.SpectrumAnalyzer( ...
    'SpectrumType',    'Power density', ...
    'SpectralAverages', 10, ...
    'YLimits',         [-150 -60], ...
    'Title',           'Received Baseband LTE Signal Spectrum', ...
    'YLabel',          'Power spectral density');
%% reshaping the cell for PDSCH to get a matrix.
% Since the PDSCH information was stored into a cell, to reform the matrix
% with all values, the subframes would be individually pulled out from the
% cell and the matrices would be merged together. Note that subframe 0 and
% 5 were not included in d_total.
% 
% d1 = req.getPDSCH{:,1};                    % Subframe 0
% d2 = req.getPDSCH{:,2};                    % Subframe 1
% d3 = req.getPDSCH{:,3};                    % Subframe 2
% d4 = req.getPDSCH{:,4};                    % Subframe 3
% d5 = req.getPDSCH{:,5};                    % Subframe 4
% d6 = req.getPDSCH{:,6};                    % Subframe 5
% d7 = req.getPDSCH{:,7};                    % Subframe 6
% d8 = req.getPDSCH{:,8};                    % Subframe 7
% d9 = req.getPDSCH{:,9};                    % Subframe 8
% d10 = req.getPDSCH{:,10};                  % Subframe 9
% d_total = [d2,d3,d4,d5,d6,d7,d8,d9,d10];   % Contains PDSCH data for subframes 1,2,3,4,6,7,8,9
% 
% %% Sampling of information being encoded back into a binary stream and compounded.
% 
% %[angles,powers] = cart2pol(real(req.getPBCH(decdata1:decdata2)),...       
%     %imag(req.getPBCH(decdata1:decdata2)));                                % Obtaining powers for PBCH 
% 
% %testingbindata = dec2bin(typecast(powers,'uint8'),8);                     % Creating the 8bit binary
% %testingdata = reshape((testingbindata-'0').',1,[]).';                     % Creating binary stream
% 
% 
% [angles1,powers1] = cart2pol(real(req.getPDCCH(decdata3:decdata4,...      
%     decdata5)),imag(req.getPDCCH(decdata3:decdata4,decdata5)));           % Obtaining powers for PDCCH
% 
% testingbindata1 = dec2bin(typecast(powers1,'uint8'),8);                   % Creating the 8bit binary
% testingdata1 = reshape((testingbindata1-'0').',1,[]).';                   % Creating binary stream
% 
% 
% [angles2,powers2] = cart2pol(real(d_total(decdata6:decdata7,decdata8))... 
%     ,imag(d_total(decdata6:decdata7,decdata8)));                          % Obtaining powers for PDSCH.
% 
% testingbindata2 = dec2bin(typecast(powers2,'uint8'),8);                   % Creating the 8bit binary
% testingdata2 = reshape((testingbindata2-'0').',1,[]).';                   % Creating binary stream\
% 
% %compilation of data into one stream.
% total_message_in_polar = [powers1;powers2];                        % Total sampled data
% compound_data = [testingdata1;testingdata2];                  % Creating total binary stream of sampled data
compound_data= [1;0;0;1;0;0;1;0];
%%  Initialize SDR device
ue = struct; % Create empty structure for transmitter
ue.SDRDeviceName ='ZedBoard and FMCOMMS2/3/4'; % Set SDR Device
radio1 = sdrdev(ue.SDRDeviceName); % Create SDR device object
% Connect to the SDR device, and get device info
devInfo1 = radio1.info;

%% Creating the Transmitter for the UE
%Bandwidth (NDLRB) must be greater than or equal to allocations
ue.RC = 'A4-6';                          % RC Configuration
ue.DesiredCenterFrequency = 2.1e9; %Same Band for downlink.
ue.NTxAnts = 1;
ue.TotFrames = 1;
ue.NCellID = 88;
ue_max = lteRMCUL(ue);
tr1BlkSize = ue_max.PUSCH.TrBlkSizes;
ue_max.TotFrames = ceil(numel(compound_data)/sum(tr1BlkSize(:)));
ue_max.TotSubframes = ue_max.TotFrames*10;

% Now use lteRMCUL to populate other parameter fields
 
fprintf('\nGenerating LTE transmit waveform:\n')
fprintf('  Packing data into %d frame(s).\n\n', ...
    ue_max.TotFrames);
ue_max.Gain = -10;
ue_max.CellRefP = ue.NTxAnts;

[rxULWaveform,rxGridy,uplink_params] = lteRMCULTool(ue_max,compound_data);
% Now we process the data to be sent to the transmitter.
% fprintf('\nGenerating LTE transmit waveform:\n')
% fprintf('  Packing image data into %d subframe(s).\n\n', ue_max.TotSubframes);

% If using an FMCOMMS4, set number of TX antennas to 1 as there is only one
% channel available...
if ~isempty(strfind(devInfo1.RFBoardVersion, 'AD-FMCOMMS4-EBZ')) && (ue.NTxAnts ~= 1)
    fprintf('\nFMCOMMS4 detected: Changing number of transmit antennas to 1.\n');
    ue.NTxAnts = 1;
end

%% Prep for transmit

sdrTransmitter1 = sdrtx(ue.SDRDeviceName);
sdrTransmitter1.BasebandSampleRate = uplink_params.SamplingRate; 
sdrTransmitter1.CenterFrequency = uplink_params.DesiredCenterFrequency;
sdrTransmitter1.ShowAdvancedProperties = true;
sdrTransmitter1.BypassUserLogic = true;
sdrTransmitter1.Gain = uplink_params.Gain;

% Apply TX channel mapping
fprintf('Setting channel map to ''1''.\n\n');
sdrTransmitter1.ChannelMapping = 1;
powerScaleFactor1 = 0.8;
rxULWaveform = rxULWaveform.*(1/max(abs(rxULWaveform))*powerScaleFactor1);

% Cast the transmit signal to int16 ---
% this is the native format for the SDR hardware.
rxULWaveform = int16(rxULWaveform*2^15);
transmitRepeat(sdrTransmitter1, rxULWaveform);

%%
rxsim1 = struct;
rxsim1.RadioFrontEndSampleRate = sdrTransmitter1.BasebandSampleRate; % Configure for same sample rate
                                                       % as transmitter
rxsim1.RadioCenterFrequency = ue.DesiredCenterFrequency;
rxsim1.NRxAnts = ue.NTxAnts;
rxsim1.FramesPerBurst = ue_max.TotFrames+1; % Number of LTE frames to capture in each burst.
                                          % Capture 1 more LTE frame than transmitted to
                                          % allow for timing offset wraparound...
rxsim1.numBurstCaptures = 1; % Number of bursts to capture

% Derived parameters
samplesPerFrame1 = 10e-3*rxsim1.RadioFrontEndSampleRate; % LTE frames period is 10 ms

rxsim1.SDRDeviceName = ue.SDRDeviceName;

sdrReceiver1 = sdrrx(rxsim1.SDRDeviceName);
sdrReceiver1.BasebandSampleRate = rxsim1.RadioFrontEndSampleRate;
sdrReceiver1.CenterFrequency = rxsim1.RadioCenterFrequency;
sdrReceiver1.SamplesPerFrame = samplesPerFrame1;
sdrReceiver1.OutputDataType = 'double';
sdrReceiver1.EnableBurstMode = true;
sdrReceiver1.NumFramesInBurst = rxsim1.FramesPerBurst;

% Configure RX channel map
if rxsim1.NRxAnts == 2
    sdrReceiver1.ChannelMapping = [1,2];
else
    sdrReceiver1.ChannelMapping = 1;
end
% burstCaptures holds sdrReceiver.FramesPerBurst number of consecutive frames worth
% of baseband LTE samples. Each column holds one LTE frame worth of data.
burstCaptures1 = zeros(samplesPerFrame1,rxsim1.NRxAnts,rxsim1.FramesPerBurst);


%% Receiver for Uplink
enb_rx.PUSCH = ue_max.PUSCH;
enb_rx.DuplexMode = 'FDD';
enb_rx.CyclicPrefix = 'Normal';
enb_rx.CellRefP = ue_max.CellRefP;
enb_rx.NCellID = ue_max.NCellID;
enb_rx.RNTI = ue_max.RNTI;
%enb_rx.NFrame = ue_max.NFrame;
enb_rx.NSubframe = 0;
% Bandwidth: {1.4 MHz, 3 MHz, 5 MHz, 10 MHz, 20 MHz}
SampleRateLUT = [1.92 3.84 7.68 15.36 30.72]*1e6;
NULRBLUT = [6 15 25 50 100];
enb_rx.NULRB = NULRBLUT(SampleRateLUT==rxsim1.RadioFrontEndSampleRate);
if isempty(enb_rx.NULRB)
    error('Sampling rate not supported. Supported rates are %s.',...
            '1.92 MHz, 3.84 MHz, 7.68 MHz, 15.36 MHz, 30.72 MHz');
end
fprintf('\nSDR hardware sampling rate configured to capture %d LTE RBs.\n',enb_rx.NULRB);

%% Channel estimation configuration structure
cc.PilotAverage = 'UserDefined'; % Type of pilot averaging
cc.FreqWindow = 9;              % Frequency averaging windows in REs
cc.TimeWindow = 1;               % Time averaging windows in REs
cc.InterpType = 'cubic';         % Interpolation type
cc.Reference = 'Antennas';       % Reference for channel estimation
cc.Window = 'Centered';
%%
enb_rxDefault = enb_rx;

while rxsim1.numBurstCaptures
        % Set default LTE parameters
    enb_rx = enb_rxDefault;

    % SDR Capture
    fprintf('\nStarting a new RF capture.\n\n')
    len1 = 0;
    for frame1 = 1:rxsim1.FramesPerBurst
        while len1 == 0
            % Store one LTE frame worth of samples
            [data1,len1,lostSamples1] = sdrReceiver1();
            burstCaptures1(:,:,frame1) = data1;
        end
        if lostSamples1
            warning('Dropped samples');
        end
        len1 = 0;
    end
    ULrxWaveform = burstCaptures1(:);
    spectrumScope1.SampleRate = rxsim1.RadioFrontEndSampleRate;
    spectrumScope1(ULrxWaveform);
    
    %% Perform frequency offset correction 
    frequencyULOffset = lteFrequencyOffset(enb_rx,ULrxWaveform);
    rxnWaveform = lteFrequencyCorrect(enb_rx,ULrxWaveform,frequencyULOffset);
    fprintf('\nCorrected a frequency offset of %i Hz.\n',frequencyULOffset)
    
    %% Perform the timing offset
    [frameULOffset,corr] =lteULFrameOffset(enb_rx,enb_rx.PUSCH,rxnWaveform);
     
    %% Sync the captured samples to the start of an LTE frame, and trim off
    % any samples that are part of an incomplete frame.
    rxnWaveform = rxnWaveform(1+frameULOffset:end);
    ULtailSamples = mod(length(rxnWaveform),samplesPerFrame1);
    rxnWaveform = rxnWaveform(1:end-ULtailSamples,:);
    enb_rx.NSubframe = 0;
    fprintf('Corrected a timing offset of %i samples.\n',frameULOffset)    
    
    %% Receiver 
    % Perform SCFDMA Demodulation
    rxnewGrid = lteSCFDMADemodulate(enb_rx,rxnWaveform);
    refnewGrid = lteULResourceGrid(enb_rx);
    % Estimate the channel on the middle 6 RBs 
    [ul_hest,ul_nest] = lteULChannelEstimate(enb_rx,enb_rx.PUSCH,cc,rxnewGrid,refnewGrid);
    ULnumFullFrames = floor(length(rxnWaveform)/samplesPerFrame1);
    enb_rx.NSubframe = 0;
    recFrames1 = zeros(ULnumFullFrames,1);
    sfDims1 = lteResourceGridSize(enb_rx);
    Lsf1 = sfDims1(2); %OFDM Symbols per subframe
    LFrame1 = 10*Lsf1; %OFDM Symbols per Frame
    rxnewSymbols = [];
            

    for frame1 = 0:(ULnumFullFrames-1)
            fprintf('\nPerforming UL-SCH Decode for frame %i of %i in burst:\n', ...
            frame1+1,ULnumFullFrames)
        
        
            enb_rx.NULRB = min(enb_rxDefault.NULRB,enb_rx.NULRB);

            % Store received frame number
            %recFrames(frame+1) = enb_rx.NFrame;       

            for sf1=0:9
               
                if sf1~=5
                    enb_rx.NSubframe = sf1;
                    rxnewsf = rxnewGrid(:,frame1*LFrame1+sf1*Lsf1+(1:Lsf1),:);
                    [ul_hestsf,ul_nestsf] = lteULChannelEstimate(enb_rx,enb_rx.PUSCH,cc,rxnewsf);
        
        % Decode PUCCH1
                    pucch1indices = ltePUCCH1Indices(enb_rx,enb_rx.PUSCH);
                   
        % Decode PUCCH2
                    pucch2Indices = ltePUCCH2Indices(enb_rx,enb_rx.PUSCH);
                    [pucch2Rx,pucch2Hest]=lteExtractResources(...
                        pucch2Indices, rxnewsf, ul_hestsf); 
                    PUCCH2 = ltePUCCH2Decode(enb_rx,enb_rx.PUSCH,pucch2Rx);
                    
        % Decode PUCCH3
                    pucch3Indices = ltePUCCH3Indices(enb_rx,enb_rx.PUSCH);
                    [pucch3Rx,pucch3Hest]=lteExtractResources(...
                        pucch3Indices, rxnewsf, ul_hestsf); 
                    PUCCH3 = ltePUCCH3Decode(enb_rx,enb_rx.PUSCH,pucch3Rx);
       
        % Obtain PUSCH data
                    outLen1 = enb_rx.PUSCH.TrBlkSizes(enb_rx.NSubframe+1);
                    puschIndices = ltePUSCHIndices(enb_rx, enb_rx.PUSCH); 
                    [puschRx, puschHest] = lteExtractResources(...
                        puschIndices, rxnewsf, ul_hestsf); 
                    
        % Perform Minimum Mean Squared Error (MMSE) Equalization
                    puschRx_MMSE = lteEqualizeMMSE(puschRx,puschHest,...
                        ul_nestsf);
                               
        % Decode PUSCH 
                    [ulschBits,rxnewsyms] = ltePUSCHDecode(enb_rx,...
                        enb_rx.PUSCH,puschRx_MMSE, puschHest, ul_nestsf);                 
                   
                    rxnewSymbols = [rxnewSymbols;rxnewsyms];%#ok
                    
        % Decode UL-SCH
                     softbuffer = [];%#ok
                     [decnewbits{sf1+1}, blknewcrc(sf1+1),softbuffer] = ...
                         lteULSCHDecode(enb_rx,enb_rx.PUSCH,...
                         outLen1, ulschBits); %#ok
                   
                end 
            end
            % Build back the decoded bits
                    
            rxnewdata = [];
            for i = 1:length(decnewbits)
                if i~=6
                    rxnewdata = [rxnewdata; decnewbits{i}(:)]; %#ok<AGROW>
                end
            end
            fprintf('  Retrieving decoded transport block data.\n');
            rxnewDataFrame(:,frame1+1) = rxnewdata; %#ok
    end
    rxsim1.numBurstCaptures = rxsim1.numBurstCaptures-1;
end
release(sdrTransmitter1);
release(sdrReceiver1);
release(spectrumScope1);
% Recombine received data blocks (in correct order) into continuous stream
[~,frameIdx] = min(recFrames1);
decodedRxDataStream1 = zeros(length(rxnewDataFrame(:)),1);
frameLen = size(rxnewDataFrame,1);
for n=1:ULnumFullFrames
    currFrame = mod(frameIdx-1,ULnumFullFrames)+1; % Get current frame index
    decodedRxDataStream1((n-1)*frameLen+1:n*frameLen) = rxnewDataFrame(:,currFrame);
    frameIdx = frameIdx+1; % Increment frame index
end

%% Creating back the Message Information.
 str10  = decodedRxDataStream1(1:length(compound_data));
% str10 = reshape(sprintf('%d',decodedRxDataStream1(1:length(compound_data))), 8, []).';
% message_in_polar= typecast(uint8(bin2dec(str10)),'double');
bitErrorRate = comm.ErrorRate;
err = bitErrorRate(decodedRxDataStream1(1:length(compound_data)), compound_data);
fprintf('  Bit Error Rate (BER) = %0.5f.\n', err(1));
fprintf('  Number of bit errors = %d.\n', err(2));
fprintf('  Number of transmitted bits = %d.\n',length(compound_data));
% figure(2)
% pspectrum(message_in_polar,ue_max.SamplingRate);
% spectrumScope1.SampleRate = ue_max.SamplingRate;
% spectrumScope1(message_in_polar);
% release(spectrumScope1);