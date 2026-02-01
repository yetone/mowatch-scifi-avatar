# ---------------------------------- #
#    GCC Bulid command log config    #
# ---------------------------------- #
#CMD_LOG = 1

# echo suspend
ifdef CMD_LOG
  NO_ECHO = 
else
  NO_ECHO = @
endif

SYSTEM := $(filter Windows_NT, $(OS))

# ---------------------------------- #
# Project name                       #
# ---------------------------------- #
PROJECT_NAME := MoWatchAPP

# ---------------------------------- #
# Path config                        #
# ---------------------------------- #
TOP_DIR     := ../..
PROJECT_DIR := ../code
OBJECT_DIR  := ./objects

# ---------------------------------- #
# Toolchain config                   #
# ---------------------------------- #
TOOLCHAIN := arm-none-eabi

CC      := $(TOOLCHAIN)-gcc
AS      := $(TOOLCHAIN)-as
LD      := $(TOOLCHAIN)-ld
OBJDUMP := $(TOOLCHAIN)-objdump
OBJCOPY := $(TOOLCHAIN)-objcopy
SIZE    := $(TOOLCHAIN)-size

# ---------------------------------- #
# ld/lib config                      #
# ---------------------------------- #
LD   := ./app.ld
LD_C := $(TOP_DIR)/libs/syscall_gcc.txt
# ---------------------------------- #
# Source files config                #
# ---------------------------------- #
SRC_FILES += $(TOP_DIR)/libs/init_datas.c 
SRC_FILES += $(TOP_DIR)/libs/tiny-json.c 
SRC_FILES += $(PROJECT_DIR)/app_main.c 

INC_PATH += -I"$(TOP_DIR)/include" 
INC_PATH += -I"$(PROJECT_DIR)" 

# ----------------------------------- #
# Objects files common to all targets #
# ----------------------------------- #
BASE_SRC  = $(notdir $(SRC_FILES)) 
BASE_OBJS = $(BASE_SRC:%.c=%.o)
OBJS      = $(BASE_OBJS:%.o=$(OBJECT_DIR)/%.o)

BASE_ElF  = $(OBJECT_DIR)/$(PROJECT_NAME).elf

# ---------------------------------- #
# Source files path                  #
# ---------------------------------- #
VPATH = $(dir $(SRC_FILES)) 


# ---------------------------------- #
# C flags common to all targets      #
# ---------------------------------- #
CFLAGS += -mcpu=cortex-m3
CFLAGS += -mthumb
CFLAGS += -O2
CFLAGS += -fmessage-length=0 -fsigned-char
CFLAGS += -ffunction-sections -fdata-sections
CFLAGS += -g3
CFLAGS += -std=gnu11

# ---------------------------------- #
# LD flags common to all targets     #
# ---------------------------------- #
LDFLAGS += -mcpu=cortex-m3
LDFLAGS += -mthumb
LDFLAGS += -O2
LDFLAGS += -ffunction-sections -fdata-sections
LDFLAGS += -g3
LDFLAGS += -Xlinker --gc-sections
LDFLAGS += --specs=nosys.specs -u _printf_float


# ---------------------------------- #
# all target list                    #
# ---------------------------------- #
all: Target_Path Target_OBJS Target_ELF Target_DONE

# ---------------------------------- #
# Create Path                        #
# ---------------------------------- #
Target_Path :
	$(shell if [ ! -d $(OBJECT_DIR) ];then mkdir $(OBJECT_DIR); fi)

# ---------------------------------- #
# compile .c .s                      #
# ---------------------------------- #
Target_OBJS : $(OBJS)

$(OBJECT_DIR)/%.o : %.c
	$(info Bulid: compiling $^)
	$(NO_ECHO)$(CC) $(CFLAGS) $(INC_PATH) -c -o  $@ $<

$(OBJECT_DIR)/%.o : %.s
	$(info Bulid: compiling $^)
	$(NO_ECHO)$(CC) $(CFLAGS) $(INC_PATH) -c -o  $@ $<

# ---------------------------------- #
# Create Image File                  #
# ---------------------------------- #
Target_ELF : $(BASE_ElF)

$(BASE_ElF) : $(OBJS)
	$(NO_ECHO)$(CC) $(LDFLAGS) -T $(LD) -T $(LD_C) -Wl,-Map=$(PROJECT_NAME).map -o $(OBJECT_DIR)/$(PROJECT_NAME).elf $^ $(LIB)
	$(NO_ECHO)$(OBJCOPY) -O binary -S $(OBJECT_DIR)/$(PROJECT_NAME).elf $(PROJECT_NAME).bin
	$(NO_ECHO)$(OBJCOPY) -O ihex   -S $(OBJECT_DIR)/$(PROJECT_NAME).elf $(PROJECT_NAME).hex
	$(NO_ECHO)$(OBJDUMP) -D $(OBJECT_DIR)/$(PROJECT_NAME).elf > $(PROJECT_NAME).dis
	$(info Bulid: creating $(OBJECT_DIR)/$(PROJECT_NAME).elf)
	$(info Bulid: creating $(PROJECT_NAME).map)
	$(info Bulid: creating $(PROJECT_NAME).bin)
	$(info Bulid: creating $(PROJECT_NAME).hex)
	$(info Bulid: creating $(PROJECT_NAME).dis)

# ---------------------------------- #
# Output image file size             #
# ---------------------------------- #
.PHONY : Target_DONE
Target_DONE:
	@echo Bulid: Output image file info:
	$(NO_ECHO)$(SIZE) $(OBJECT_DIR)/$(PROJECT_NAME).elf
	@echo Bulid: $(PROJECT_NAME) make done.

# ---------------------------------------- #
# delete file(.o .elf .bin .dis .hex .map) #
# ---------------------------------------- #
.PHONY : clean

clean :
	$(NO_ECHO)rm -rf $(OBJECT_DIR) *.elf *.bin *.dis *.hex *.map
	@echo delete *.o *.elf *.bin *.dis *.hex *.map
