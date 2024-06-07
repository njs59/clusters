writerObj = gif('SineWave.gif');
open(writerObj);
nFrame=10000;
hfig = figure('color','w','un','pix','pos',[360 550 450 400]);
axis([0 2*pi -1.5 1.5])
hold on;
time = linspace(0,2*pi,nFrame);
for nt=1:nFrame   
    plot(time(nt),sin(time(nt)),'marker','*');
%     mov(nt) = getframe(gcf);
%     writeVideo(writerObj,mov(nt));
      mov = getframe(gcf);
      writeVideo(writerObj,mov);
end
close(writerObj)