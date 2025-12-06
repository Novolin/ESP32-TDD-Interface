# ESP32-based TDD/TTY Adapter

I got a wicked deal on an Ultratec Miniprint a while ago, and I've been wanting to do something useful with it. With my Hoembrew Computer slowly taking shape, I realized that the W65C51 serial adapter has support for Baudot encoding, meaning all I would need is a way to decode the audio, and then I can realize my dreams of having a beepyboopy keyboard system for a computer interface. 

My current roadmap is to get the ESP to read data first, since that's the hardest part of this whole procedure, after which everything else will be building off my existing knowledge of Baudot and FSK encoding. 

I hope to use I2S sound equipment, since I have some from a previous stab at this, but worst case scenario, I will just deal with raw microphone data. An ESP32 has I2S compatibility, and should be able to handle everything I need, and then some, without issue.