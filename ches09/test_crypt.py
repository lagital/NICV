import des_block


msg= des_block.des_block("42c331daf2e07d88", 64)
key= des_block.des_block("6a64786a64786a64", 64)
print "msg", msg
print "key", key
print "cryptogram", msg.encipher(key)