%%% Uplink Waveform Modeling Using SRS and PUCCH 

% %% UE Configuration
ue = struct;
ue.NULRB = 15;                  % Number of resource blocks
ue.NCellID = 10;                % Physical layer cell identity
ue.Hopping = 'Off';             % Disable frequency hopping
ue.CyclicPrefixUL = 'Normal';   % Normal cyclic prefix
ue.DuplexMode = 'FDD';          % Frequency Division Duplex (FDD)
ue.NTxAnts = 1;                 % Number of transmit antennas
ue.NFrame = 0;                  % Frame number

% %% PUCCH Configuration
pucch = struct;
% Vector of PUCCH resource indices, one per transmission antenna
pucch.ResourceIdx = 0:ue.NTxAnts-1; 
pucch.DeltaShift = 1;               % PUCCH delta shift parameter
pucch.CyclicShifts = 0;             % PUCCH delta offset parameter
pucch.ResourceSize = 0;             % Size of resources allocated to PUCCH

% %% SRS Configuration

% The cell-specific configuration means that for this cell, two
% opportunities for SRS transmission exist within each frame, subframes 0
% and 5. All UEs in the cell must shorten their Physical Uplink Control
% Channel (PUCCH) transmissions during these subframes to allow for SRS
% reception without interference, even if they are not transmitting SRS
% themselves. The UE-specific configuration means that this UE is
% configured to generate SRS only in subframe 0.

srs = struct;           
srs.NTxAnts = 1;        % Number of transmit antennas
% Cell-specific SRS configuration has 5ms periodicity with an offset of
% 0 (signaled by |srs.SubframeConfig = 3| as indicated in TS36.211

srs.SubframeConfig = 3; % Cell-specific SRS period = 5ms, offset = 0
srs.BWConfig = 6;       % Cell-specific SRS bandwidth configuration
srs.BW = 0;             % UE-specific SRS bandwidth configuration
srs.HoppingBW = 0;      % SRS frequency hopping configuration
srs.TxComb = 0;         % Even indices for comb transmission
srs.FreqPosition = 0;   % Frequency domain position
% The UE-specific SRS configuration has 10ms periodicity with an offset
% of 0 (signaled by |srs.ConfigIdx = 7| as indicated in TS36.213

srs.ConfigIdx = 7;      % UE-specific SRS period = 10ms, offset = 0
srs.CyclicShift = 0;    % UE-cyclic shift

% %% Subframe Loop
% The processing loop generates a subframe at a time. These are all
% concatenated to create the resource grid for a frame (10 subframes).
% The loop functions as:

% 1)--- _SRS Information_: By calling <matlab:doc('lteSRSInfo') lteSRSInfo> we
% can get information related to SRS for a given subframe. The
% |IsSRSSubframe| field of the structure |srsDims| returned from the
% <matlab:doc('lteSRSInfo') lteSRSInfo> call indicates if the current
% subframe (given by |ue.NSubframe|) is a cell-specific SRS subframe
% (|IsSRSSubframe = 1|) or not (|IsSRSSubframe = 0|). The value of this
% field can be copied into the |ue.Shortened| field. This ensures that the
% subsequent PUCCH generation will correctly respect the cell-specific SRS
% configuration for all subframes, omitting the last symbol of the PUCCH in
% the cell-specific SRS subframes.
%
% 2)--- _PUCCH 1 Demodulation Reference Signal (DRS) Generation and Mapping_:
% The DRS signal is located in the 3rd, 4th and 5th symbols of each slot
% and therefore never has the potential to collide with the SRS.
%
% 3)--- _PUCCH 1 Generation and Mapping_: Unlike the DRS, the PUCCH 1
% transmission can occupy the last symbol of the subframe unless
% |ue.Shortened = 1|. In this case the last symbol of the subframe will be
% left empty.

txGrid = [];    % Create empty resource grid

for i = 1:10    % Process 10 subframes

        % Configure subframe number (0-based)
        ue.NSubframe = i-1;
        fprintf('Subframe %d:\n',ue.NSubframe);

        % Establish if this subframe is a cell-specific SRS subframe,
        % and if so configure the PUCCH for shortened transmission
        srsInfo = lteSRSInfo(ue, srs);
        ue.Shortened = srsInfo.IsSRSSubframe; % Copy SRS info to ue struct          

        % Create empty uplink subframe    
        txSubframe = lteULResourceGrid(ue);

        % Generate and map PUCCH1 DRS to resource grid
        drsIndices = ltePUCCH1DRSIndices(ue, pucch);% DRS indices
        drsSymbols = ltePUCCH1DRS(ue, pucch);       % DRS sequence
        txSubframe(drsIndices) = drsSymbols;        % Map to resource grid

        % Generate and map PUCCH1 to resource grid     
        pucchIndices = ltePUCCH1Indices(ue, pucch); % PUCCH1 indices
        ACK = [0; 1];                               % HARQ indicator values
        pucchSymbols = ltePUCCH1(ue, pucch, ACK);   % PUCCH1 sequence
        txSubframe(pucchIndices) = pucchSymbols;    % Map to resource grid
        if (ue.Shortened)
            disp('Transmitting shortened PUCCH');
        else
            disp('Transmitting full-length PUCCH');
        end

        % Configure the SRS sequence group number (u) according to TS
        % 36.211 Section 5.5.1.3 with group hopping disabled
        srs.SeqGroup = mod(ue.NCellID,30);

        % Configure the SRS base sequence number (v) according to TS 36.211
        % Section 5.5.1.4 with sequence hopping disabled
        srs.SeqIdx = 0;
        
        % Generate and map SRS to resource grid
        % (if active under UE-specific SRS configuration)
        [srsIndices, srsIndicesInfo] = lteSRSIndices(ue, srs);% SRS indices
        srsSymbols = lteSRS(ue, srs);                         % SRS seq.
        if (srs.NTxAnts == 1 && ue.NTxAnts > 1) % Map to resource grid
            % Select antenna for multiple antenna selection diversity 
            txSubframe( ...     
                hSRSOffsetIndices(ue, srsIndices, srsIndicesInfo.Port)) = ...
                srsSymbols;
        else
            txSubframe(srsIndices) = srsSymbols;
        end
        % Message to console indicating when SRS is mapped to the resource
        % grid.
        if(~isempty(srsIndices))
            disp('Transmitting SRS');
        end

        % Concatenate subframes to form frame
        txGrid = [txGrid txSubframe]; %#ok
end

%%% Results
% The figure produced shows the number of active subcarriers in each
% SC-FDMA symbol across the 140 symbols in |txGrid|. All SC-FDMA symbols
% contain 12 active subcarriers corresponding to the single resource block
% bandwidth of the PUCCH except:
%
% 1)--- symbol 13, the last symbol of subframe 0 which has 48 active
% subcarriers corresponding to an 8 resource block SRS transmission
% 2)--- symbol 83, the last symbol of subframe 5 which has 0 active subcarriers
% corresponding to the shortened PUCCH (last symbol empty) to allow for
% potential SRS transmission by another UE in this cell.

figure;
for i = 1:ue.NTxAnts
    subplot(ue.NTxAnts,1,i);
    plot(0:size(txGrid,2)-1,sum(abs(txGrid(:,:,i)) ~= 0),'r:o')
    xlabel('symbol number');
    ylabel('active subcarriers');
    title(sprintf('Antenna %d',i-1));
end

% Plot the resource grid with the PUCCH at the band edges and the SRS comb
% transmission in subframe 0.
figure;
pcolor(abs(txGrid));
colormap([1 1 1; 0 0 0.5])
shading flat;
xlabel('SC-FDMA symbol'); ylabel('subcarrier')

% The output at the MATLAB command window when running this example
% shows PUCCH transmission in all 10 subframes, with shortening in
% subframes 0 and 5, and an SRS transmission in subframe 0.
            

sss = txGrid(:,14);  %%% Taking only srs part of transmitted signal

%%%% Introducing Channel-1 with noise where noise_1 will represent the 
%    noise & changes in channel due to object
snr_db_1 = 11;
snr_1 = 10^(snr_db_1/10);
noise_1 = 1/sqrt(2*snr_1) * (randn(size(txGrid)) +1i*randn(size(txGrid)));
%%%% srs with noise-1 addition
rx_srs_noise_1 = noise_1 + txGrid;

sss1 = rx_srs_noise_1(:,14); %%% Taking only srs part of received signal

figure;
pcolor(abs(rx_srs_noise_1));
colormap([1 1 1; 0 0 0.5])
shading flat;
xlabel('SC-FDMA with noise-1 symbol'); ylabel('subcarrier');



%%%% Channel-2 with noise where noise_2 will represent the 
%    noise & changes in channel due to object
snr_db_2 = 15;
snr_2 = 10^(snr_db_2/10);
noise_2 = 1/sqrt(2*snr_2) * (randn(size(txGrid)) +1i*randn(size(txGrid)));
%%%% srs with noise-2 addition
rx_srs_noise_2 = noise_2 + txGrid;

sss2 = rx_srs_noise_2(:,14);  %%% Taking only srs part of received signal
figure;
pcolor(abs(rx_srs_noise_2));
colormap([1 1 1; 0 0 0.5])
shading flat;
xlabel('SC-FDMA with noise-2 symbol'); ylabel('subcarrier');


sss3 = xcorr(sss1, sss2)
%sss4 = sss - sss3;










