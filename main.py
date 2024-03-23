import os, customtkinter as CTk

CTk.set_appearance_mode('system')                 # Modes: "system" (default), "dark", "light"
CTk.set_default_color_theme('blue')             # Themes: "blue" (standard), "green", "dark-blue"

app = CTk.CTk()
app.geometry('600x600')
app.title("CTkEMU")
app.resizable(False, False)

vmName = CTk.StringVar()
diskSize = CTk.StringVar()
ramSize = CTk.StringVar()
cdRomPath = CTk.StringVar()
vDrivePath = CTk.StringVar()
platform = CTk.StringVar()
coresNum = CTk.StringVar()
bootMode = CTk.StringVar()

bootArg = "d"

bootModes = ['CD-ROM drive',
             'Hard drive']

platforms = ['x86_64',
             'i386']

cpuCores = ["1"]
ghasda = 0
coresArg = 1

coreCount = str(os.cpu_count())

while(int(cpuCores[-1]) < int(coreCount)):
    cpuCores.append(str(ghasda + 2))
    ghasda += 2

# print(cpuCores)

def chooseFile(stringVar: CTk.StringVar):
    stringVar.set(str(CTk.filedialog.askopenfilename()))

def getInfo():
    print(str(diskSize.get()))
    print(str(ramSize.get()))
    print(str(cdRomPath.get()))
    print(str(vDrivePath.get()))
    print(str(bootMode.get()))

def createDrive():
    os.mkdir(f'{vmName.get()}')
    os.system(f'qemu-img create -f qcow2 "{vmName.get()}/{vmName.get()}.qcow2" {diskSize.get()}G')

def launchVm(bootorder: CTk.StringVar):
    command = f"qemu-system-{platform.get()}"
    Args = [f"-m {ramSize.get()}"]
    if (bootorder.get() == "CD-ROM drive"):
        Args.append(f'-cdrom "{cdRomPath.get()}"')
        bootArg = "d"
    elif (bootorder.get() == "Hard drive"):
        bootArg = "c"
        if (cdRomPath.get != ""):
            Args.append(f'-cdrom "{cdRomPath.get()}"')

    if(coresNum.get() != "0"):
        cores = coresNum.get()
    Args.append(f'-hda "{vDrivePath.get()}"')
    Args.append(f'-smp {cores}')
    Args.append(f'-boot {bootArg}')

    for arg in Args:
        command = command + f" {arg}"

    print(f'executing <{command}>')
    os.system(command)


###############
# Main window #
###############

CTk.CTkLabel(app, text="VM name:", font=CTk.CTkFont(family='Calibri Bold')).grid(row=0, column=0, padx=20, pady=20, sticky='w')
CTk.CTkEntry(app, width=250, placeholder_text="40", textvariable=vmName).grid(row=0, column=1, sticky='w')

CTk.CTkLabel(app, text="QEMU Disk size (in GBytes):", font=CTk.CTkFont(family='Calibri Bold')).grid(row=1, column=0, padx=20, sticky='w')
CTk.CTkEntry(app, width=70, placeholder_text="40", textvariable=diskSize).grid(row=1, column=1, sticky='w')
CTk.CTkButton(app, width=20, text="Create disk", command=createDrive).grid(row=1, column=2, padx=10, sticky='w')

CTk.CTkLabel(app, text="RAM size (in MBytes):", font=CTk.CTkFont(family='Calibri Bold')).grid(row=2, column=0, padx=20, pady=20, sticky='w')
CTk.CTkEntry(app, width=70, placeholder_text="512", textvariable=ramSize).grid(row=2, column=1, sticky='w')

CTk.CTkLabel(app, text="CPU cores:", font=CTk.CTkFont(family='Calibri Bold')).grid(row=3, column=0, padx=20, sticky='w')
CTk.CTkOptionMenu(app, values=cpuCores, variable=coresNum).grid(row=3, column=1, sticky='w')

CTk.CTkLabel(app, text="Path to CD-ROM image:", font=CTk.CTkFont(family='Calibri Bold')).grid(row=4, column=0, padx=20, pady=20, sticky='w')
CTk.CTkEntry(app, width=300, state="disabled", textvariable=cdRomPath).grid(row=4, column=1, sticky='w')
CTk.CTkButton(app, width=20, text="...", command=lambda:chooseFile(cdRomPath)).grid(row=4, column=2, padx=10, sticky='w')

CTk.CTkLabel(app, text="Path to virtual drive:", font=CTk.CTkFont(family='Calibri Bold')).grid(row=5, column=0, padx=20, sticky='w')
CTk.CTkEntry(app, width=300, state="disabled", textvariable=vDrivePath).grid(row=5, column=1, sticky='w')
CTk.CTkButton(app, width=20, text="...", command=lambda:chooseFile(vDrivePath)).grid(row=5, column=2, padx=10, sticky='w')

CTk.CTkLabel(app, text="Platform:", font=CTk.CTkFont(family='Calibri Bold')).grid(row=6, column=0, padx=20, pady=20, sticky='w')
CTk.CTkOptionMenu(app, values=platforms, variable=platform).grid(row=6, column=1, sticky='w')

CTk.CTkLabel(app, text="Boot from:", font=CTk.CTkFont(family='Calibri Bold')).grid(row=7, column=0, padx=20, sticky='w')
CTk.CTkOptionMenu(app, values=bootModes, variable=bootMode).grid(row=7, column=1, sticky='w')

'''
CTk.CTkButton(app, text="Save VM Configuration", command=getInfo).grid(row=8, column=0, padx=20, pady=20, sticky='w')
CTk.CTkButton(app, text="Start-up VM", command=lambda:launchVm(bootMode)).grid(row=8, column=1, sticky='w')
'''

app.mainloop()
