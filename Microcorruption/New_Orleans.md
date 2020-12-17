# New Orleans

## Target
Our goal in this task is to open the *LockIT Pro a.01*.

## What we already know
We know from the description, that we have to supply a password and must restart the system after setting the password.
The controller used is a MSP430.

## Behaviour analysis
First let us run the program and take a look at its behaviour.

The Program starts in a halted state.
When **c**ontinuing the program we are prompted to enter a password.
Let us try the password *test*.
If we take a look at the I/O Console, we can see that we are prompted the following information:
```
Invalid password; try again.
```

So this did not work then. But we do know now, that there must be a password set already. Also we know that the password entered by us must be checked against the formerly set password.

Now let us set a Breakpoint at an interesting address.
If we take a look at the Disassembly information, we can see that just before the string "Enter the password to continue" is moved into r15, there is a call of \<create password\>. This looks kind of suspicious. Let us set a breakpoint there at address **443c**

**Reset** the controller and **c**ontinue until we hit the breakpoint.
Let us **s**tep to the next instruction.

\<create password\> seems not to be doing much, it simply moves some hex values into r15. Those values are **0x2E 0x30 0x54 0x3D 0x40 0x39 0x31 0x00**. Let us take a look what happens next. Lets set another breakpoint at address **444a**. If we **c**ontinue now, we will skip the <puts> method used to output the "Enter the password to continue" prompt. This method should not be of high interest for us at the moment. 

Let us **s**tep through it. This method calls \<getsn\>. This seems to be the method responsible to promt for the password. Let us input *test* again.
Let's **s**tep further. Having a look at the Live Memory Dump, we can see that *test* is written to **439C til 439F**. So that is what should be tested against the correct password. Lets note this mentally. 

When **s**tepping a few more times we see the call to \<check_password\> let us see how the password is checked. We notice, that **439C** is still held in r15. It is moved to r13 and subsequently r14 is added to r13. r14 is zero at the moment so this does not change anything. Next the value at address **439C** (which is the first character of the password we choose) is compared to whatever is at address 0x2400. This could already be the password we are looking for! 
**.0T=@91** is our candidate for the password. Before we try it however, let us see what happens next. JNE is executed which jumps if the zero bit is not set. Zero is not set at the moment so this should result in a jump to <check_password+0x16> which is equal to address **44D2** causing the register r15 to be reset and the execution of a ret command. It seems like the password check has failed at this point.

Let us try the string we found earlier in order to open the lock. It seems to be pretty clear that this must be the data the method \<check_password\> is comparing against. Let us **reset** the controller and **c**ontinue without breakpoints. When prompted to input the password we input the found string **.0T=@91** or the hex values **0x2E 0x30 0x54 0x3D 0x40 0x39 0x31 0x00** found even earlyer (you need to tick the checkbox if you are going with the hex values). We **c**ontinue again and get the prompt "Door Unlocked". 

The last thing to do now is to follow the instructions, **reset** the controller and type **solve** in order to open the lock. Type the password one last time and we are in!

### Further Notes on this Challenge
The function \<check_password\> uses r15 as storage for the starting address of the password typed in by the user. r13 holds the address of the character (or byte) which will be checked next. r14 is incremented every time a correct input is detected and added to r13 when the next character has to be checked. This results in r13 pointing to the next character to be checked after r14 is added to r13. If r14 reaches the value 8, this loop is broken wich tells us that the maximum password length is 8 characters. Before exiting after detection of a correct password, r15 is set to 1. r15 does serve as a flag to indicate a successful password authentication.