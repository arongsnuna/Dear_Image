PROMPT = """Think step by step to carry out the instruction.

Emoji Options: 
:p = face_with_tongue
8) = smiling_face_with_sunglasses
:) = smiling_face
;) = winking_face

Instruction: Hide the face of Nicole Kidman with :p
Program:
OBJ0=FACEDET(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='face_with_tongue')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Hide the faces of Nicole Kidman and Brad Pitt with ;) and 8)
Program:
OBJ0=FACEDET(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Nicole Kidman',category=None)
IMAGE0=EMOJI(image=IMAGE,object=OBJ1,emoji='winking_face')
OBJ2=SELECT(image=IMAGE,object=OBJ0,query='Brad Pitt',category=None)
IMAGE1=EMOJI(image=IMAGE0,object=OBJ1,emoji='smiling_face_with_sunglasses')
FINAL_RESULT=RESULT(var=IMAGE1)

Instruction: Create a color pop of Amy and Daphne
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='Amy,Daphne',category=None)
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the girl and the umbrella
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='girl,umbrella',category=None)
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the dog, frisbee, and grass
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='dog,frisbee,grass',category=None)
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the man wearing a red suit (person)
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='man wearing a red suit',category='person')
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Create a color pop of the man wearing a red suit (person)
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='man wearing a red suit',category='person')
IMAGE0=COLORPOP(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Select person wearing glass and blur
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='wearing glass',category='person')
IMAGE0=BGBLUR(image=IMAGE,object=OBJ1,background='False')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Replace the red bus with a blue bus
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Replace the red bus with blue bus and the road with dirt road
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
OBJ2=SEG(image=IMAGE0)
OBJ3=SELECT(image=IMAGE0,object=OBJ2,query='road',category=None)
IMAGE1=REPLACE(image=IMAGE0,object=OBJ3,prompt='dirt road')
FINAL_RESULT=RESULT(var=IMAGE1)

Instruction: Replace the red bus (bus) with a truck
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category='bus')
IMAGE0=REPLACE(image=IMAGE,object=OBJ1,prompt='blue bus')
FINAL_RESULT=RESULT(var=IMAGE0)

# 수정 - 예시문 추가
Instruction: Select ground and remove background
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='ground')
IMAGE0=REMOVEBG(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Select ground and delete background
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='ground')
IMAGE0=REMOVEBG(image=IMAGE,object=OBJ1)
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Select the red bus, blue bus and blur the background
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus,blue bus',category=None)
IMAGE0=BGBLUR(image=IMAGE,object=OBJ1,background='True')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Select the red bus and blur the background
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=BGBLUR(image=IMAGE,object=OBJ1,background='True')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Select the red bus and blur
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus',category=None)
IMAGE0=BGBLUR(image=IMAGE,object=OBJ1,background='False')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: Select the red bus, blue bus and blur
Program:
OBJ0=SEG(image=IMAGE)
OBJ1=SELECT(image=IMAGE,object=OBJ0,query='red bus, blue bus',category=None)
IMAGE0=BGBLUR(image=IMAGE,object=OBJ1,background='False')
FINAL_RESULT=RESULT(var=IMAGE0)

Instruction: {instruction}
Program:
"""