import customtkinter as ctk
'''Note that most of the variables are not required.
Example:
'text_color' if not defined, the deffault colour will appear.'''

# Window
window = ctk.CTk()
window.title('customtkinter app')
window.geometry('600x400')

# Widgets: Label
label = ctk.CTkLabel(
    window,
    width         = 150,
    height        = 45,
    corner_radius = 10,
    fg_color      = '#677D6A',
    text          = 'Test label',
    text_color    = '#D6BD98',
    font          = ("Times New Roman", 16, "bold"))
label.pack()
''' The above can also be written in a different way (see the example below), 
but generally, everything is listed vertically for better structure.
(This also applies to the widgets.)

Example:
label = ctk.CTkLabel(window, width = 150, height = 45, corner_radius = 10, fg_color = '#677D6A', text = 'Test label', text_color = '#D6BD98', font = ("Times New Roman", 16, "bold"))
label.pack '''

# Widgets: Button
button = ctk.CTkButton(
    window,
    width          = 120, 
    height         = 32,
    corner_radius  = 10, 
    border_width   = 0, 
    border_spacing = 3,  
    fg_color       = '#677D6A', 
    hover_color    = '#1A3636',
    border_color   = '#1A3636',
    text           = 'Colour mode', 
    text_color     = '#D6BD98',
    font           = ("Times New Roman", 16, "bold"),
    command        = lambda: ctk.set_appearance_mode('light'))
button.pack(padx = 20, pady = 10)

# Widgets: Frame
frame = ctk.CTkFrame(
    window, 
    fg_color     = '#40534C',
    border_color = '#1A3636')
frame.pack()

# Widgets: Slider
slider = ctk.CTkSlider(
    frame,
    width              = 200,
    height             = 15,
    border_width       = 5,
    from_              = 0,
    to                 = 100,
    number_of_steps    = 10,
    fg_color           = '#677D6A',
    progress_color     = '#D6BD98',
    border_color       = '#1A3636',
    button_color       = '#D6BD98',
    button_hover_color = '#C2A374',
    orientation        = 'horizontal')
slider.pack(padx=10, pady=10)

# Widgets: Switch
switch = ctk.CTkSwitch(
    window,
    width              = 30,
    height             = 15,
    switch_width       = 30,
    switch_height      = 15,
    corner_radius      = 10,
    border_width       = 5,
    button_length      = 0.05,
    fg_color           = '#677D6A',
    border_color       = '#1A3636',
    button_color       = '#D6BD98',
    button_hover_color = '#C2A374')
switch.pack()

# Run
window.mainloop()