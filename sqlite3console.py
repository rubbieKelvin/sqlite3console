import os, sqlite3, sys
from terminaltables import ascii_table

__author__ = 'rubbie kelvin voltsman'

class SQLite3Console(object):
	"""docstring for SQLite3Console"""
	def __init__(self):
		super(SQLite3Console, self).__init__()
		self.ps1 = 'sqlite3>'
		self.ps2 = '...'
		self.ps = self.ps1
		self.close_signal = 'exit'
		self.command_line = ''
		self.running = False

	def run_from_file(self, db_file, sqlfile):
		try:
			db_conn = sqlite3.connect(db_file)
			db_cursor = db_conn.cursor()
			self.cli_out('connection established : %s' %(db_file))
			self.cli_out('reading %s' %(sqlfile))

			with open(sqlfile) as f:
				content = f.read()
				content = content.split('\n')

			for command in content:
				if command:
					if command.endswith(';'):
						self.ps = self.ps1
						self.command_line = self.command_line+' '+command
						command = self.command_line
						self.command_line = ''
						try:
							command = command.strip()
							db_cursor.execute(command)
							db_conn.commit()
							if command.lstrip().upper().startswith('SELECT'):
								res = ascii_table.AsciiTable(db_cursor.fetchall())
								print(res.table)

						except sqlite3.Error as e:
							print('error:', e.args[0])
					else:
						self.ps = self.ps2
						self.command_line = self.command_line+' '+command.strip('\n')
			db_conn.commit()
			db_conn.close()
		except Exception as e:
			print('error:', e)

	def run(self, db_file):
		try:
			db_conn = sqlite3.connect(db_file)
			db_cursor = db_conn.cursor()
			self.cli_out('connection established : %s' %(db_file))
			self.cli_out('type "%s" to save and close connection safely' %(self.close_signal))

			self.running = True

			while self.running:
				#...
				command = self.cli_in('')

				if command == self.close_signal:
					self.quit()
				elif command:
					if command.endswith(';'):
						self.ps = self.ps1
						self.command_line = self.command_line+' '+command
						command = self.command_line
						self.command_line = ''
						try:
							command = command.strip()
							db_cursor.execute(command)
							db_conn.commit()
							if command.lstrip().upper().startswith('SELECT'):
								res = ascii_table.AsciiTable(db_cursor.fetchall())
								print(res.table)

						except sqlite3.Error as e:
							print('error:', e.args[0])
					else:
						self.ps = self.ps2
						self.command_line = self.command_line+' '+command.strip('\n')
				else:
					pass
			db_conn.commit()
			db_conn.close()
		except Exception as e:
			print('error: ', e)

	def quit(self):
		self.running = False

	def cli_out(self, text):
		print('%s %s' %(self.ps1, text))

	def cli_in(self, prompt):
		return input('%s %s' %(self.ps, prompt))


app = SQLite3Console()

if len(sys.argv) > 2:
	sqlfile = sys.argv[2]
	if sqlfile.endswith('.sql'):
		# start running commands
		app.run_from_file(db_file=sys.argv[1], sqlfile=sqlfile)
		pass
	else:
		raise Exception("%s is not an sql file" % sqlfile)
elif len(sys.argv) > 1:
	app.run(sys.argv[1])
else:
	db = input('Enter db file name: ')
	app.run(db)