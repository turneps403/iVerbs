import os,sys,tty,termios
import os
import select as something
import curses.ascii as keycode
class _GetKey:
	@classmethod
	def await_tap(cls):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = ''
			block = None
			while True:
				fd_sets = something.select([sys.stdin.fileno()], [], [], block)
				if len(fd_sets[0]) > 0:
					ch_chunk = os.read(sys.stdin.fileno(), 1)
					ch += ch_chunk.decode("utf-8")
					block = 0
				else:
					break
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

class _GetLine:
	@classmethod
	def await_for_enter(cls, tap_action=None):
		term_line = ''
		while True:
			tap_key = _GetKey.await_tap()
			if tap_action and tap_action.get(tap_key, None):
				# just one action and go back
				if tap_key.isprintable():
					print_key = tap_key if not tap_key.endswith("\n") else tap_key[:-1]
					print(print_key, end='', flush=True)
				action = tap_action.get(tap_key)
				if action.get("action", None):
					action.get("action")(term_line)
				if action.get("break", 0) > 0:
					break
			elif not tap_key.isprintable():
				tap_code = ord(tap_key[:1])
				if tap_code in [keycode.BS, keycode.DEL]:
					print("\b \b", end='', flush=True)
				elif tap_code == keycode.CR:
					term_line += tap_key
					break
				elif tap_code in [keycode.ETX, keycode.EOT, keycode.SUB]: # Ctrl+ C,D,Z
					sys.exit()
				elif tap_code == keycode.ESC and len(tap_key) == 1: # ESC
					sys.exit()
			elif tap_key.endswith("\n"):
				print(tap_key[:-1], end='', flush=True)
				term_line += tap_key[:-1]
				break
			else:
				print(tap_key, end='', flush=True)
				term_line += tap_key 
		return term_line


def get():
	inkey = _Getch()
	while(1):
		k=inkey()
		if k != '':
			break
	if k=='\x1b[A':
		print("up")
	elif k=='\x1b[B':
		print("down")
	elif k=='\x1b[C':
		print("right")
	elif k=='\x1b[D':
		print("left")
	else:
		if k.isprintable():
			sys.stdout.write(k + '*')
			sys.stdout.flush()
			#print(k)
		else:
			#print("not printable: "+str(ord(k)))
			print("not printable: "+k)
		#print("not an arrow key!")
		#print(k + "*")

def main():
	_GetLine.await_for_enter()
	#for i in range(0,10):
	#	get()
	#	#ee = input("sss:")

if __name__=='__main__':
        main()
