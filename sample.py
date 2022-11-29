from indictrans import Transliterator

trn = Transliterator(source='hin', target='eng', build_lookup=True)

hin = "मेरे तीन आर्डर है एक में पूमा का शर्ट है दूसरे में रीबॉक का शूज है साइज है 366 मुझे 34 चाहिए था"
eng = trn.transform(hin)
print(eng)



