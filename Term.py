import os,sys,tty,termios
import select as watcher
import curses.ascii as keycode

class GetKey:
	@classmethod
	def await_tap(cls):
		fd = sys.stdin.fileno()
		cur_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = ''
			block = None
			while True:
				fd_sets = watcher.select([sys.stdin.fileno()], [], [], block)
				if len(fd_sets[0]) > 0:
					ch_chunk = os.read(sys.stdin.fileno(), 1)
					ch += ch_chunk.decode("utf-8")
					block = 0
				else:
					break
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, cur_settings)
		return ch

class GetLine:
	@classmethod
	def await_for_enter(cls, tap_action=None):
		right_position = 0
		term_line = ''
		while True:
			tap_key = GetKey.await_tap()
			if not tap_key.isprintable():
				if tap_key == '\x1b[D':
					# left arrow
					if right_position < len(term_line):
						right_position += 1
						print("\b", end='', flush=True)
						continue
				elif tap_key == '\x1b[C':
					# right arrow
					if right_position > 0:
						print(term_line[(len(term_line) - right_position):(len(term_line) - right_position + 1)], end='', flush=True)
						right_position -= 1
						continue
				
				tap_code = ord(tap_key[:1])
				if tap_code in [keycode.BS, keycode.DEL]:
					print("\b \b", end='', flush=True)
				elif tap_code == keycode.CR:
					if right_position > 0:
						print_key = term_line[(len(term_line) - right_position):len(term_line)]
						print(print_key, end='', flush=True)
					term_line += tap_key
					break
				elif tap_code in [keycode.ETX, keycode.EOT, keycode.SUB]: # Ctrl+ C,D,Z
					sys.exit()
				elif tap_code == keycode.ESC and len(tap_key) == 1: # ESC
					sys.exit()
			else:
				if right_position == 0:
					print(tap_key, end='', flush=True)
					term_line += tap_key 
				else:
					print_key = tap_key + term_line[(len(term_line) - right_position):len(term_line)]
					print(print_key + "\b"*right_position, end='', flush=True)
					term_line = term_line[0:(len(term_line) - right_position)] + tap_key + term_line[(len(term_line) - right_position):len(term_line)]

			if tap_action and tap_action.get(tap_key, None):
				# just one action and go back
				action = tap_action.get(tap_key)
				if action.get("action", None):
					action.get("action")(term_line)
				if action.get("break", 0) > 0:
					break
			
		return term_line

if __name__=='__main__':
	GetLine.await_for_enter()
