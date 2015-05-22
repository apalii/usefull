import paramiko

# SSH access using pkey snippet 
# alias nit='ssh -p 14889 -i ~/Desktop/GIT/nitrous action@euw1.nitrousbox.com'

k = paramiko.RSAKey.from_private_key_file('/home/apalii/Desktop/GIT/nitrous')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('euw1.nitrousbox.com', username='action', port=14889, pkey=k)
stdin, stdout, stderr = client.exec_command('mkdir qweqweqwwe')
client.close()
