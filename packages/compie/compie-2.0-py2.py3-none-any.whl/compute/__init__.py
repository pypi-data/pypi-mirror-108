#Made with ❤️ on Python 3.8.10 by Whirlpool-Programmer
'''
Compute (c) 2021 Whirlpool-Programmer
Version: 2.0
Summary: A Python module made for use with numbers and data
email: Whirlpool.programmer@outlook.com
Made by Whirlpool-Programmer
'''
'''
LIST OF AVALIABLE FUNCTIONS AND CLASSES:

FUNCTIONS:
make_penguin()				added in version 1.0
isprime(number)				added in version 2b1
ratio(int,int)				added in version 2b1  >> bugfix 2.0
factorial(int)				added in version 0.1b
arithmetic_mean(list)		added in version 1.4
decimal2binary(int)			added in version 1.6.1
binary2decimal(int)			added in version 1.6.2
decimal2octal(int)			added in version 1.6.3
octal2decimal(int)			added in version 1.6.4
hexadecimal2decimal(str)	added in version 1.6.5
decimal2hexadecimal(int)	added in version 1.6.6
evaluate(str)				added in version 0.1b

CLASSES:
decimal(value)				added in version 2b0
binary(value)				added in version 2b0
octal(value)				added in version 2b0
hexadecimal(value)			added in version 2b0
'''

def make_penguin():
    import tkinter
    window = tkinter.Tk()
    txt = tkinter.Label(window, text="now.. you are also cute and also a penguin!! Go use my module!", font=[("Segoe"),(15)])
    txt.place(x = 0,y =0)
    window.mainloop()

def isprime(number):
	respected_primes = [2,3,5,7]
	if number == 1:
		return ValueError("1 is neither prime nor composite.")
	else:
		if number in respected_primes:
			return True
		else:
			if number%2 != 0 and number%3 != 0 and number%5 != 0 and number%7 != 0:
				return True
			else:
				return False

def ratio(first,second):
	if first != float and second != float:
		for i in range(first if first > second else second,0,-1):
				if first%i == 0 and second%i == 0:
					first = first/i
					second = second/i
		return str(int(first))+":"+str(int(second))
	else:
		raise ValueError("You cannot enter floats for ratio.")

def factorial(num):
    if num == 1:
        return 1
    else:
        return num * factorial(num - 1)

def arithmetic_mean(nums):
    nums = list(nums)
    mean = 0
    for num in nums:
        mean = mean + num
    
    return mean/len(nums)

def decimal2binary(decimal):
    decimal = int(decimal)
    binary = ''
    while decimal != 0:
        binary = binary + str(decimal % 2)
        decimal = decimal // 2
    return binary [::-1]

def binary2decimal(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

def hexadecimal2decimal(hexadecimal):
    conversion_table = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10 , 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    hexadecimal = hexadecimal.strip().upper()
    decimal = 0
    power = len(hexadecimal) -1
    for digit in hexadecimal:
        decimal += conversion_table[digit]*16**power
        power -= 1
    return decimal

def decimal2hexadecimal(decimal):
    conversion_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A' , 'B', 'C', 'D', 'E', 'F']
    decimal = int(decimal)
    hexadecimal = ''
    while(decimal>0):
        remainder = decimal%16
        hexadecimal = conversion_table[remainder]+ hexadecimal
        decimal = decimal//16
    return hexadecimal

def octal2decimal(octal):
    decimal = 0
    octnum = str(octal)
    length = len(octnum)
    for x in octnum:
        length = length-1
        decimal += pow(8,length) * int(x)
    return decimal

def decimal2octal(decimal):
    decimal = int(decimal)
    octal = 0
    ctr = 0
    temp = decimal
    while(temp > 0):
        octal += ((temp%8)*(10**ctr))
        temp = int(temp/8)
        ctr += 1
    return octal

def evaluate(command):
        if "factorial(" in command:
            com = command.lower()
            fac_num_st = com.find("factorial(") + len("factorial(")
            fac_num_ed = com.find(")")
            fac_cmd_st = com.find("factorial(")
            fac_cmd_ed = com.find(")")
            fac_cmd = com[fac_cmd_st:fac_cmd_ed]
            fac_num = com[fac_num_st:fac_num_ed]        
            fac = factorial(int(fac_num))
            command.replace(fac_cmd,str(fac))
        if "fac(" in command:
            com = command.lower()
            fac_num_st = com.find("fac(") + len("fac(")
            fac_num_ed = com.find(")")
            fac_cmd_st = com.find("fac(")
            fac_cmd_ed = com.find(")")
            fac_cmd = com[fac_cmd_st:fac_cmd_ed]
            fac_num = com[fac_num_st:fac_num_ed]        
            fac = factorial(int(fac_num))
            command.replace(fac_cmd,str(fac))
        if "pi" in command.lower():
            command  = command.replace("pi", str(3.141592653589793))
        return eval(command)


class decimal:
	"""
	The Decimal Class
	initial value must be a decimal
	example: [decimal_of_10 = decimal(10)]

	variables included:
	value [the value of the decimal] example: decimal(10).value
	dec [decimal of value] example: decimal(10).dec
	bin [binary of value] example: decimal(10).bin
	oct [octal of value] example: decimal(10).oct
	hex [hexadecimal of value] example: decimal(10).hex
	"""

	def __init__(self, value):
		self.value = value
		self.dec = self.value
		self.bin = decimal2binary(self.value)
		self.oct = decimal2octal(self.value)
		self.hex = decimal2hexadecimal(self.value)
	
	def setvalue(self, value,numtype = "decimal"):
		if numtype == "decimal" or numtype == "dec":
			self.value = value
		elif numtype == "binary" or numtype == "bin":
			self.value = binary2decimal(value)
		elif numtype == "octal" or numtype == "oct":
			self.value = octal2decimal(value)
		elif numtype == "hexadecimal" or numtype == "hex":
			self.value = hexadecimal2decimal(value)
		else:
			raise SyntaxError("undefined type {}".format(numtype))

class binary:
	"""
	The Binary Class
	initial value must be a binary [starting character must not be "0"]
	example: [binary_of_10 = binary(1010)]

	variables included:
	value [the value of the binary (in binary)] example: binary(1010).value
	dec [decimal of value] example: binary(1010).dec
	bin [binary of value] example: binary(1010).bin
	oct [octal of value] example: binary(1010).oct
	hex [hexadecimal of value] example: binary(1010).hex
	"""

	def __init__(self, value):
		self.value = value
		self.dec = binary2decimal(self.value)
		self.bin = self.value
		self.oct = decimal2octal(binary2decimal(self.value))
		self.hex = decimal2hexadecimal(binary2decimal(self.value))
	def setvalue(self, value,numtype = "binary"):
		if numtype == "decimal" or numtype == "dec":
			self.value = decimal2binary(value)
		elif numtype == "binary" or numtype == "bin":
			self.value = value
		elif numtype == "octal" or numtype == "oct":
			self.value = decimal2binary(octal2decimal(value))
		elif numtype == "hexadecimal" or numtype == "hex":
			self.value = decimal2binary(hexadecimal2decimal(value))
		else:
			raise SyntaxError("undefined type {}".format(numtype))

class octal:
	"""
	The Octal Class
	initial value must be a octal
	example: [octal_of_10 = octal(12)]

	variables included:
	value [the value of the octal (in octal)] example: octal(12).value
	dec [decimal of value] example: octal(12).dec
	bin [binary of value] example: octal(12).bin
	oct [octal of value] example: octal(12).oct
	hex [hexadecimal of value] example: octal(12).hex
    """
	def __init__(self, value):
		self.value = value
		self.dec = octal2decimal(self.value)
		self.bin = decimal2binary(octal2decimal(self.value))
		self.oct = self.value
		self.hex = decimal2hexadecimal(octal2decimal(self.value))
	
	def setvalue(self, value,numtype = "octal"):
		if numtype == "decimal" or numtype == "dec":
			self.value = decimal2octal(value)
		elif numtype == "binary" or numtype == "bin":
			self.value = decimal2octal(binary2decimal(value))
		elif numtype == "octal" or numtype == "oct":
			self.value = value
		elif numtype == "hexadecimal" or numtype == "hex":
			self.value = decimal2octal(hexadecimal2decimal(value))
		else:
			raise SyntaxError("undefined type {}".format(numtype))

class hexadecimal:
	"""
	The Hexadecimal Class
	initial value must be a hexadecimal [and also a string]
	example: [hexadecimal_of_10 = hexadecimal("A")]

	variables included:
	value [the value of the hexadecimal] example: hexadecimal("A").value
	dec [decimal of value] example: hexadecimal("A").dec
	bin [binary of value] example: hexadecimal("A").bin
	oct [octal of value] example: hexadecimal("A").oct
	hex [hexadecimal of value] example: hexadecimal("A").hex
	"""

	def __init__(self, value):
		self.value = value
		self.dec = hexadecimal2decimal(self.value)
		self.bin = decimal2binary(hexadecimal2decimal(self.value))
		self.oct = decimal2octal(hexadecimal2decimal(self.value))
		self.hex = self.value
	
	def setvalue(self, value,numtype = "decimal"):
		if numtype == "decimal" or numtype == "dec":
			self.value = decimal2hexadecimal(value)
		elif numtype == "binary" or numtype == "bin":
			self.value = decimal2hexadecimal(binary2decimal(value))
		elif numtype == "octal" or numtype == "oct":
			self.value = decimal2hexadecimal(octal2decimal(value))
		elif numtype == "hexadecimal" or numtype == "hex":
			self.value = value
		else:
			raise SyntaxError("undefined type {}".format(numtype))

'''
BUILD COMMANDS
python setup.py sdist
python setup.py bdist_wheel --universal
python -m twine upload dist/*.*
'''
print(ratio(10,51390))
__version__ = "2.0"
__author__ = 'Whirlpool-Programmer'
__credits__ = ['Whirlpool-Programmer','Sapphire Corp.']
pi = 3.141592653589793