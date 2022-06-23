from tkinter.tix import Tree
from main_my_functions import *



#source = 'dv2.MOV'

save_video = False # want to save video? (when video as source)
show_video=False # set true when using video file
save_img=True  # set true when using only image file to save the image
# when using image as input, lower the threshold value of image classification

cap = cv2.imread(r'3.jpg')
frame = cv2.resize(cap, frame_size)  # resizing image
original_frame = frame.copy()
frame, results = object_detection(frame) 
print(results, 1)

rider_list = []
head_list = []
number_list = []

for result in results:
	x1,y1,x2,y2,cnf, clas = result
	if clas == 0:
		rider_list.append(result)
	elif clas == 1:
		head_list.append(result)
	elif clas == 2:
		number_list.append(result)
		#print(number_list)
	print(1, number_list)

for rdr in rider_list:
	time_stamp = str(time.time())
	x1r, y1r, x2r, y2r, cnfr, clasr = rdr
	for hd in head_list:
		x1h, y1h, x2h, y2h, cnfh, clash = hd
		if inside_box([x1r,y1r,x2r,y2r], [x1h,y1h,x2h,y2h]): # if this head inside this rider bbox
			try:
				head_img = original_frame[y1h:y2h, x1h:x2h]
				helmet_present = img_classify(head_img)
				print("rider ",helmet_present)
			except:
				helmet_present[0] = None
			if  helmet_present[0] == True: # if helmet present
				frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0,255,0), 1)
				frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
				frame = cv2.putText(frame, "Helmet Worn", (x1h, y1h+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 0), 1, cv2.LINE_AA)
			elif helmet_present[0] == None: # if helmet absent 
				frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
				frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
				frame = cv2.putText(frame, "Helmet Absent", (x1h, y1h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
			elif helmet_present[0] == False: # Poor prediction
				frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
				frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
				frame = cv2.putText(frame, "No Helmet", (x1h, y1h+60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
				print("false  .....")
			
				try:
					cv2.imwrite(f'riders_pictures/{time_stamp}.jpg', frame[y1r:y2r, x1r:x2r])
				except:
					print('could not save rider')

				print('S',number_list)
				for num in number_list:
					x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
					if inside_box([x1r,y1r,x2r,y2r], [x1_num, y1_num, x2_num, y2_num]):
						try:
							num_img = original_frame[y1_num:y2_num, x1_num:x2_num]
							cv2.imwrite(f'number_plates/{time_stamp}_{conf_num}.jpg', num_img)
						except:
							print('could not save number plate')
							

frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
cv2.imshow('Frame', frame)							
if save_img: #save img
	cv2.imwrite('saved_frame.jpg', frame)
if show_video: # show video
	frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
	cv2.imshow('Frame', frame)


cv2.waitKey(0) & 0xFF == ord('q')
cv2.destroyAllWindows()
print('Execution completed')

