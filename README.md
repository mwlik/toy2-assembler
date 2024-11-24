A [TOY/2](https://www.pcengines.ch/toy2.htm) assembler I've made while trying to solve the TOY/2 challenge in SECCON2024.

Format:
```asm
section .data:
	lol 0xFF0
	lol2 0xA
section .text:
	LDA lol
	ADC lol2 ; what does this even do?
	ILL
```
