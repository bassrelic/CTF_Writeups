# Sydney

## Target
Our goal in this task is to open the *LockIT Pro a.01*.

## What we already know
We know from the description, that we have to supply a password and must restart the system after setting the password.
The controller used is a MSP430.
If we need any information regarding the Instruction Set, we will have a look at *SLAU144J MSP430x2xx FamilyUser's Guide*

In this new version (Revision 02) the password is not stored in memory anymore, preventing the attack done in New Orleans in the past.

## Behaviour analysis
First off, let us have a look at the behaviour of the program when running it as intended without the use of Breakpoints. We **c**ontinue the code execution and get prompted to input a password. After inserting the password *test* and **c**ontinuing the excution, we are promted with the message:
```
Invalid password; try again.
```
So the code does behave the same as before from the outside. No information gained there it seems.

Now let us have a look at the subroutines called in *main*. The first routine of interest is \<check_password\> let us set a breakpoint there, **c**ontinue the execution and **s**tep through the code. We enter *test* as password and **c**ontinue to the breakpoint. Now we **s**tep through the code to understand how the entered password is checked in this new revision. 

We see that *R15* is compared to the value *0x6b23*. After execution, the *N* bit is set. Note here, that the actual value checked against is not *0x6b23* but rather *236b*, meaning that the first and second words are switched (You can see this in the disassembly or current instruction window). We keep this in mind. The next instruction is a jump (*jnz*) which would jump to *44ac* if the zero bit is not set. If the zero bit is set, the next value would be checked. This means, that we have to supply a password which statisfies these compares. We now check the following cmp statements and can find the following sequence:
**236b727c6d716066**
This Sequence should enable us to open the lock.

Let us **reset** and **c**ontinue the program. Now when asked to input the password, simply paste the formerly found string. Do not forget to tick the checkbox in oder to enter hex values.

We are in!

Now type **solve** and paste the same string when prompted to supply a password.

### Further Notes on this Challenge
Indeed, the password is not stored in code anymore. Due to the way it is programmed, we can find the password in the assembly code itself. Is this more secure than before? I do not think so.
We can also see, that the supplied password is eight characters long.