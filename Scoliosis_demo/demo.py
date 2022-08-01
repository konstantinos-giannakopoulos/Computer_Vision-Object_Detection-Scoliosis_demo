from tkinter import *
# loading Python Imaging Library
from PIL import ImageTk,Image
#from PIL.Image import core as _imaging
# To get the dialog box to open when required 
from tkinter import filedialog, ttk

import sys, os
from pathlib import Path
import pandas as pd
import subprocess
from shutil import copyfile

#import hello
import run_ssd_example
import estimate_Cobb_angle
import run_sagittal_example
import estimate_Sagittal


#def resource_path(relative_path):
#    if hasattr(sys, '_MEIPASS'):
#        return os.path.join(sys._MEIPASS, relative_path)
#    return os.path.join(os.path.abspath("."), relative_path)

#def resource_path(relative_path):
#    if getattr(sys, 'frozen', False):
#        # If the application is run as a bundle, the PyInstaller bootloader
#        # extends the sys module by a flag frozen=True and sets the app 
#        # path into variable _MEIPASS'.
#        application_path = sys._MEIPASS
#        return os.path.join(sys._MEIPASS, relative_path)
#    else:
#        application_path = os.path.dirname(os.path.abspath(__file__))
#        return os.path.join(os.path.abspath("."), relative_path)
#        print('>> >>> >> ', application_path)

def resource_path(relative_path):
    application_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(application_path, relative_path)

#application_path = os.path.dirname(os.path.abspath(__file__))
#print(application_path)
#cwd = os.getcwd()
#print('cwd ', cwd)
#dir_path = os.path.dirname(os.path.realpath(__file__))
#print('dir_path ', dir_path)


# Create a window
root = Tk()
# Set Title as Image Loader
root.title("Scoliosis")
# Set the resolution of window
root.geometry("1400x800")
# Allow Window to be resizable
root.resizable(width = False, height = False)


#Label(root, text = '', font =(
#  'Verdana', 15)).pack(side = TOP, pady = 1)
#  
## Creating a photoimage object to use image
#photo = PhotoImage(file = r"utils\logo.png")
#  
## here, image option is used to
## set image on button
#Button(root, text = 'Click Me !', width=20, height=20, image = photo).pack(side = TOP)

tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)


tabControl.add(tab1, text ='Frontal View')
tabControl.add(tab2, text ='Sagittal View')
tabControl.pack(expand = 1, fill ="both")


# show company logo
output_image = resource_path('utils/full_logo.jpg')
img = Image.open(output_image) # open an image
img = img.resize((200, 50), Image.ANTIALIAS) # resize the image and apply a high-quality down sampling filter
img = ImageTk.PhotoImage(img) # PhotoImage class is used to add image to widgets, icons etc
#panel1 = Label(tab1, image = img) # create a label
#panel1.out_image = img # set the image as img
#panel1.grid(row = 1, column = 0)
panel2 = Label(tab2, image = img) # create a label
panel2.out_image = img # set the image as img 
panel2.grid(row = 0, column = 0)


# panel report
panel_report = Label(tab1)
panel_report.grid(row = 1,column = 4)

# panel report
panel_buttons = Label(tab1)
panel_buttons.grid(row = 0,column = 0)
panel1 = Label(panel_buttons, image = img) # create a label
panel1.out_image = img # set the image as img
panel1.grid(row = 0, column = 0)

panel_images = Label(tab1)
panel_images.grid(row = 1,column = 0)

#panel_images2 = Label(tab1)
#panel_images2.grid(row = 1,column = 1)


frontal_menu_variable = StringVar(tab1)
frontal_menu_variable.set("model-1") # default value
frontal_model_menu = OptionMenu(panel_buttons, frontal_menu_variable, "model-1", "model-2")
frontal_model_menu.grid(row=0, column=3)

sagittal_menu_variable = StringVar(tab1)
sagittal_menu_variable.set("model-2") # default value
sagittal_model_menu = OptionMenu(tab2, sagittal_menu_variable, "model-2")
sagittal_model_menu.grid(row=0, column=3)













def refresh(self):
    self.destroy()
    self.__init__()
    


def openfilename():  
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename()
    return filename


def open_img():
    # Select the Imagename  from a folder 
    x = openfilename()
  
    # opens the image
    img = Image.open(x)
      
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((250, 700), Image.ANTIALIAS)
  
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)
    
    
    copyfile(x, resource_path('frontal/input_image.jpg'))
    
    ### (E)
    load_ground_truth(x)
   
    # create a label
    panel = Label(panel_images, image = img)
      
    # set the image as img 
    panel.image = img
    panel.grid(row = 0,column = 0)
    logtext = Label(panel_report, bg="azure", text="                                                                         ")
    logtext.grid(row = 10,column = 1)
    logtext = Label(panel_report, bg="azure", text="Image Loaded")
    logtext.grid(row = 10,column = 1)
    
    

def load_ground_truth(imagefilename):
    #print('>>>>>>>>>>', imagefilename)
    imagename = Path(imagefilename).stem
    #print('>>>>>>>>>>', imagename)
    
    
    file = resource_path('samples/ground-truth_Cobb-angles.csv')
    df = pd.read_csv(file)
    #print(df)
    image,ca_t,ca_l,shape = df['Image'], df['Cobb_angle_T'],  df['Cobb_angle_L'], df['Shape']
    #print(image,ca_t,ca_l,shape)
    
    image_gt = df.loc[df['Image'] == imagename]
    if(image_gt.empty):
        text_cat = 'N/A'
        text_cal = 'N/A'
        text_shape = 'N/A'
    else:
        text_cat = image_gt.iloc[0]['Cobb_angle_T']
        text_cal = image_gt.iloc[0]['Cobb_angle_L']
        text_shape = image_gt.iloc[0]['Shape']     
        
    #print(image_gt)
    #print('>>>>>>>>>>>>>', image_gt.iloc[0]['Cobb_angle_T'])
    
    logtext = Label(panel_report, bg="azure", text="                                                                      ")
    logtext.grid(row = 10,column = 1)
    logtext = Label(panel_report, bg="azure", text="Ground Truths Loaded")
    logtext.grid(row = 10,column = 1)
    
    

    
    text = Label(panel_report, bg="LightGreen", text='Ground Truth')
    text.grid(row = 2,column = 0)
    #text = Label(tab1, bg="AntiqueWhite1", text=image_gt)
    #text.grid(row = 7,column = 2)
    text = Label(panel_report, bg="LightGreen", text="Cobb angle T")
    text.grid(row = 3,column = 0)
    text = Label(panel_report, bg="LightGreen", text="                               ")
    text.grid(row = 3,column = 1)
    text = Label(panel_report, bg="LightGreen", text=text_cat)
    text.grid(row = 3,column = 1)
    text = Label(panel_report, bg="LightGreen", text="Cobb angle L")
    text.grid(row = 4,column = 0)
    text = Label(panel_report, bg="LightGreen", text="                               ")
    text.grid(row = 4,column = 1)
    text = Label(panel_report, bg="LightGreen", text=text_cal)
    text.grid(row = 4,column = 1)
    text = Label(panel_report, bg="LightGreen", text="Shape")
    text.grid(row = 5,column = 0)
    text = Label(panel_report, bg="LightGreen", text="                               ")
    text.grid(row = 5,column = 1)
    text = Label(panel_report, bg="LightGreen", text=text_shape)
    text.grid(row = 5,column = 1)
    
##########################################################################



def model_inference():
    ssd_inference = run_ssd_example
    input_image = resource_path('frontal/input_image.jpg')
    model_option = frontal_menu_variable.get()
    #print('>>>>>>>>>>>> ', model_option)
    #System.exit(-1)
    ssd_inference.main(input_image,model_option)
    return "Bounding Boxes Detected"
    
    
def open_output_img():
    
    output_image = resource_path('frontal/output_image.jpg')
    # opens the image
    img = Image.open(output_image)
      
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((250, 700), Image.ANTIALIAS)
  
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)
   
    # create a label
    panel = Label(panel_images, image = img)
      
    # set the image as img 
    panel.out_image = img
    panel.grid(row = 0, column = 1)
    logtext = Label(panel_report, bg="azure", text="                                                                      ")
    logtext.grid(row = 10,column = 1)
    logtext = Label(panel_report, bg="azure", text="Output Image Loaded")
    logtext.grid(row = 10,column = 1)
    

def open_final_output_img():
    
    output_image = resource_path('frontal/final_final_output.jpg')
    # opens the image
    img = Image.open(output_image)
      
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((250, 700), Image.ANTIALIAS)
  
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)
   
    # create a label
    panel = Label(panel_images, image = img)
      
    # set the image as img 
    panel.out_image = img
    panel.grid(row = 0, column = 2)
    logtext = Label(panel_report, bg="azure", text="                                                                      ")
    logtext.grid(row = 10,column = 1)
    logtext = Label(panel_report, bg="azure", text="Output Image Loaded")
    logtext.grid(row = 10,column = 1)
    #refresh()

    

def estimate_cobb_angle():
    ### (A)
    log_text = model_inference()
      
    text = Label(panel_report, bg="azure", text="                                                                        ")
    text.grid(row = 10,column = 1)
    text = Label(panel_report, bg="azure",  text=log_text)
    text.grid(row = 10,column = 1)
    
    
    text = Label(panel_report, text="-----------------------------")
    text.grid(row = 6,column = 0)
    #text = Label(panel_report, text="-----------------------------")
    #text.grid(row = 5,column = 1)
    #text = Label(panel_report, text="-----------------------------")
    #text.grid(row = 5,column = 2)
    
    ### (B)
    file = resource_path('frontal/output_boxes.csv')
    eCA = estimate_Cobb_angle
    num_slope_changes, shape, cobb_angles = eCA.main(file)
    print(num_slope_changes, shape, cobb_angles)
    
    rounded_cobb_angles = []
    for cobb_angle in cobb_angles:
        rounded_cobb_angles.append(round(cobb_angle,2))
    print('>>> ',rounded_cobb_angles)
    
    text = Label(panel_report, bg="AntiqueWhite1", text="Shape of Scoliosis: ")
    text.grid(row = 7,column = 0)
    text = Label(panel_report, bg="AntiqueWhite1", text=shape)
    text.grid(row = 7,column = 1)
    #text = Label(tab1, bg="AntiqueWhite1", text='-shape')
    #text.grid(row = 6,column = 2)
    logtext = Label(panel_report, bg="light sky blue", text="                                                                ")
    logtext.grid(row = 8,column = 0)
    text = Label(panel_report, bg="light sky blue", text="Cobb Angles: ")
    text.grid(row = 8,column = 0)
    text = Label(panel_report, bg="light sky blue", text=rounded_cobb_angles)
    text.grid(row = 8,column = 1)
    #text = Label(tab1, bg="light sky blue", text=' degrees')
    #text.grid(row = 7,column = 2)
    
    logtext = Label(panel_report, bg="azure", text="                                                    ")
    logtext.grid(row = 10,column = 1)
    logtext = Label(panel_report, bg="azure", text="Cobb Angle Estimated.")
    logtext.grid(row = 10,column = 1)
    
    ### (C)
    open_output_img()
    
    ### (D)
    open_final_output_img()
    #root.mainloop()
    #ttk.update(self)
    #panel_images.pack
    #refresh()
  

def refresh():
    print("refresh") 
    logtext = Label(panel_report, text="                                                                                   ")
    logtext.grid(row = 7,column = 1)           
    logtext = Label(panel_report, text="                                                                                   ")
    logtext.grid(row = 8,column = 1)
    logtext = Label(panel_report, text="                                                                                   ")
    logtext.grid(row = 10,column = 1)
    root.mainloop()



# Create a button and place it into the window using grid layout
frontal_btn = Button(panel_buttons, text ='Load an X-ray image', command = open_img).grid(
                                        row = 0, column = 1, columnspan = 1)
frontal_btn2 = Button(panel_buttons, text ='Estimate Cobb Angle', command = estimate_cobb_angle).grid(
                                        row = 0, column = 2, columnspan = 1)
refresh_btn3 = Button(panel_buttons, text ='Refresh', command = refresh).grid(
                                        row = 0, column = 4, columnspan = 1)





text = Label(panel_report, text="Report")
text.grid(row = 0,column = 0)
text = Label(panel_report, text="-----------------------------")
text.grid(row = 1,column = 0)
#text = Label(panel_report, text="-----------------------------")
#text.grid(row = 1,column = 1)
#text = Label(panel_report, text="-----------------------------")
#text.grid(row = 1,column = 2)
    
logtext = Label(panel_report, bg="azure", text="                                                                           ")
logtext.grid(row = 10,column = 0)
logtext = Label(panel_report, bg="azure", text="Log Message:     ")
logtext.grid(row = 10,column = 0)

#outLbl = Label(root)







































# SAG_OPTIONS = [
# "mb1-ssd"
# ] #etc


# sagittal_menu_variable = StringVar(tab2)
# sagittal_menu_variable.set(SAG_OPTIONS[0]) # default value

# sagittal_model_menu = MyOptionMenu(tab2, 'Select model ', *SAG_OPTIONS)
# sagittal_model_menu.grid(row=1, column=1)
# tabControl.pack()












def sag_open_img():
    # Select the Imagename  from a folder 
    x = openfilename()
  
    # opens the image
    img = Image.open(x)
      
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((250, 600), Image.ANTIALIAS)
  
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)
    
    
    copyfile(x, resource_path('sagittal/input_image.jpg'))
   
    # create a label
    panel = Label(tab2, image = img)
      
    # set the image as img 
    panel.image = img
    panel.grid(row = 2,column = 0)
    logtext = Label(tab2, bg="azure", text="                                       ")
    logtext.grid(row = 13,column = 1)
    logtext = Label(tab2, bg="azure", text="Image Loaded")
    logtext.grid(row = 13,column = 1)






def sag_inference():
    sagittal_inference = run_sagittal_example
    input_image = resource_path('sagittal/input_image.jpg')
    model_option = sagittal_menu_variable.get()
    run_sagittal_example.main(input_image,model_option)
    
    
    file = resource_path('sagittal/output_boxes.csv')
    eSag = estimate_Sagittal
    #num_slope_changes, shape, cobb_angles = eSag.main(file)
    eSag.main(file)
    #print(num_slope_changes, shape, cobb_angles)
    #(B)
    sag_open_output_img()
    #(C)
    sag_open_final_output_img()
    return "Bounding Boxes Detected"
    
    
def sag_open_output_img():
    
    output_image = resource_path('sagittal/output_image.jpg')
    # opens the image
    img = Image.open(output_image)
      
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((250, 600), Image.ANTIALIAS)
  
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)
   
    # create a label
    panel = Label(tab2, image = img)
      
    # set the image as img 
    panel.out_image = img
    panel.grid(row = 2, column = 1)
    logtext = Label(tab2, bg="azure", text="                                       ")
    logtext.grid(row = 13,column = 1)
    logtext = Label(tab2, bg="azure", text="Output Image Loaded")
    logtext.grid(row = 13,column = 1)
    
    
    
def sag_open_final_output_img():
    
    output_image = resource_path('sagittal/final_output.jpg')
    # opens the image
    img = Image.open(output_image)
      
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((250, 600), Image.ANTIALIAS)
  
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)
   
    # create a label
    panel = Label(tab2, image = img)
      
    # set the image as img 
    panel.out_image = img
    panel.grid(row = 2, column = 2)
    logtext = Label(tab2, bg="azure", text="                                                                      ")
    logtext.grid(row = 13,column = 1)
    logtext = Label(tab2, bg="azure", text="Output Image Loaded")
    logtext.grid(row = 13,column = 1)






sagittal_btn = Button(tab2, text ='Load a Sagittal View Image', command = sag_open_img).grid(
                                        row = 0, column = 1, columnspan = 1)

sagittal_btn2 = Button(tab2, text ='Estimate', command = sag_inference).grid(
                                        row = 0, column = 2, columnspan = 1)




text = Label(tab2, text="Report")
text.grid(row = 4,column = 1)
text = Label(tab2, text="-----------------------------")
text.grid(row = 12,column = 0)
text = Label(tab2, text="-----------------------------")
text.grid(row = 12,column = 1)
text = Label(tab2, text="-----------------------------")
text.grid(row = 12,column = 2)
    
logtext = Label(tab2, bg="azure", text="                                       ")
logtext.grid(row = 13,column = 0)
logtext = Label(tab2, bg="azure", text="Log Message:     ")
logtext.grid(row = 13,column = 0)




root.mainloop()

