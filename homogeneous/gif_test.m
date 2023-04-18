% 100 matrices of size 4x4 stored in cell array filled with random data
M = squeeze(mat2cell((rand(20,20,100) > 0.5)*2-1, 20, 20, ones(1,100)));
outFilename = 'myGifFile.gif';
fig = figure();
ax = axes();
colormap([0 0 0; 1 1 1]);
for i=1:100
    imagesc(ax, M{i});
    img = getframe(ax);
    img = n;
    if i==1
        imwrite(img, outFilename, 'gif', 'LoopCount', inf, 'DelayTime', 0.05)
    else
        imwrite(img, outFilename, 'gif', 'WriteMode', 'append', 'DelayTime', 0.05);
    end
end