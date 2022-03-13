clc
clear all
close all
warning off

dbstop if error
x=imread('image.png');
imshow(x);
title('Original Image');
%%
% [BW,maskedRGBImage] = createMask(x);
% figure;
% imshow(BW);
% title('Binary Image of Red color objects');
% figure;
% imshow(maskedRGBImage);
% title('Color Image of Red color objects');
% [f g]=size(BW);
% process=zeros(f,g);
% xa=imfill(BW,'holes');
% figure;
% imshow(xa);
% title('Binary mask of red color objects after hole filling');
% figure;
% [L ,num]=bwlabel(xa);
% stats1=regionprops(xa,'Area','Perimeter');
% for R=1:num
%         circularity =(4 * pi * stats1(R).Area)/(stats1(R).Perimeter^ 2) ;
%         if (circularity>=0.94)
%             process=process+(L==R);
%         end
% end
% imshow(process);
% title('Mask for red color circles');
% processa=uint8(cat(3,process,process,process));
% figure;
% imshow(x.*processa);
% title('Red color Circles');


%%

xblur1 = imgaussfilt(x,2);
imshow(xblur1)
xGray = rgb2gray(xblur1);
imshow(xGray)
xBW = imbinarize(xGray);
xBW = imfill(xBW,'holes');
imshow(xBW)
[B,L,N,A] = bwboundaries(xGray);
figure(2);
imshow(x); hold on;
colors=['b' 'g' 'r' 'c' 'm' 'y'];
%ref: https://uk.mathworks.com/help/images/ref/bwboundaries.html 
for k=1:length(B),
  boundary = B{k};
  cidx = mod(k,length(colors))+1;
  plot(boundary(:,2), boundary(:,1),...
       colors(cidx),'LineWidth',2);

  %randomize text position for better visibility
  rndRow = ceil(length(boundary)/(mod(rand*k,7)+1));
  col = boundary(rndRow,2); row = boundary(rndRow,1);
  h = text(col+1, row-1, num2str(L(row,col)));
  set(h,'Color',colors(cidx),'FontSize',14,'FontWeight','bold');
end
g = regionprops(xBW, 'Area','BoundingBox');

g(1)
area_values = [g.Area]

% %%
% colorNames = { 'red','green'};
% %colorNames = { 'red','green','purple','blue','yellow' };
% nColors = length(colorNames);
% [rows, columns, numberOfColorChannels] = size(x);
% sample_regions = false([rows columns nColors]);
% 
% 
% % Convert the fabric RGB image into an L*a*b image.
% cform = makecform('srgb2lab');
% lab_image = applycform(x,cform);
% imshow(lab_image)
% 
% % Calculate the mean 'a' and 'b' value for each area extracted.
% % These values serve as your color markers in 'a*b' space.
% a = lab_image(:,:,2);
% b = lab_image(:,:,3);
% color_markers = repmat(0, [nColors, 2]);
% 
% for count = 1:nColors
%   color_markers(count,1) = mean2(a(sample_regions(:,:,count)));
%   color_markers(count,2) = mean2(b(sample_regions(:,:,count)));
% end
% 
% % For example, the average color of the second sample region in 'a*b' space is:
% disp( sprintf('[%0.3f,%0.3f]', color_markers(2,1), color_markers(2,2)) );