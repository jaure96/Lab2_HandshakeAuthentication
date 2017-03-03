#!/usr/bin/env python3
import hashlib
gmJBRrAcFf=hashlib.sha256
import hmac
gmJBRrAcFK=hmac.compare_digest
import socket
gmJBRrAcFT=socket.TCP_NODELAY
gmJBRrAcFy=socket.socket
gmJBRrAcFL=socket.SOCK_STREAM
gmJBRrAcFl=socket.IPPROTO_TCP
gmJBRrAcFC=socket.AF_INET
import struct
gmJBRrAcFW=struct.unpack
gmJBRrAcFY=struct.pack
import random
gmJBRrAcFU=random.random
gmJBRrAcFe=random.sample
gmJBRrAcFG=random.randint
import time
gmJBRrAcFQ=time.sleep
import sys
gmJBRrAcFd=sys.argv
gmJBRrAcFn=sys.version_info
gmJBRrAcFI=sys.exit
import getopt
gmJBRrAcFE=getopt.getopt
gmJBRrAcDk=getopt.GetoptError
gmJBRrAckp={'martin.hellman':'secret1','ralph.merkle':'secret2','whitfield.diffie':'secret3'}
gmJBRrAcku=4
gmJBRrAcki=3
gmJBRrAcka=50
gmJBRrAckf=1000
gmJBRrAckK=0x00
gmJBRrAcky=0x01
gmJBRrAckC=0x02
gmJBRrAckL=0x03
gmJBRrAckl=0x04
class ConfigException(Exception):
 pass
def gmJBRrAckF(byte_array):
 return ''.join(format(x,'02x')for x in byte_array)
def gmJBRrAckD(debug_string):
 print("  >>> {}".format(debug_string))
def gmJBRrAckt():
 print("\nList of identities and passwords available in the authenticator:\n")
 for gmJBRrAckT,gmJBRrAcFw in sorted(gmJBRrAckp.items()):
  print("   * identity:\t{}\n     secret:\t{}\n".format(gmJBRrAckT,gmJBRrAcFw))
def gmJBRrAckV():
 print('''
usage:
   -rROLENAME
  --role=ROLENAME      where ROLENAME is either 'peer' or 'authenticator'
                       (without the quotation marks).
   -aIP
  --authenticator=ip   where IP is the IP address of the authenticator.
                       This parameter is mandatory for the 'peer' role.
   -pPORT
  --port=PORT          where PORT is the port where the authenticator
                       listens to. This parameter is always mandatory.
   -iIDENTITY
  --identity=IDENTITY  where IDENTITY is the identity to authenticate with.
                       This paraeter is mandatory for the 'peer' role.
   -sSECRET
  --secret=SECRET      where SECRET is the secret for the IDENTITY.
                       This parameter is mandatory for the 'peer' role.
   -lNAME
  --localname=NAME     where NAME is the name of the peer or the
                       authenticator. This parameter is always mandatory.
   -cSIZE
  --chunk=SIZE         where SIZE is the size of the packet chunk we want
                       to send over the sockets. Default value: {} octects.
   -d
  --debug              Show debugging information.
  --list-identities    List identities and secrets available in the authenticator.
   -h
  --help               Show program usage.
    '''.format(gmJBRrAcki))
def gmJBRrAckj(prompt):
 try:
  return raw_input(prompt)
 except NameError:
  return input(prompt)
def gmJBRrAckh():
 gmJBRrAckW={}
 gmJBRrAckW['role']=gmJBRrAckj("Enter role (peer or authenticator): ").lower()
 try:
  if(gmJBRrAckW['role']=='peer'):
   gmJBRrAckW['authenticator']=gmJBRrAckj("Enter the IP of the authenticator: ")
   gmJBRrAckW['port']=gmJBRrAckj("Enter the port to connect to: ")
   gmJBRrAckW['identity']=gmJBRrAckj("Enter the identity you want to authenticate with: ")
   gmJBRrAckW['secret']=gmJBRrAckj("Enter the secret you want to authenticate with: ")
   gmJBRrAckW['localname']=gmJBRrAckj("Enter the name of the local (peer) system: ")
  elif(gmJBRrAckW['role']=='authenticator'):
   gmJBRrAckW['port']=gmJBRrAckj("Enter the port to listen to: ")
   gmJBRrAckW['localname']=gmJBRrAckj("Enter the name of the local (authenticator) system: ")
  else:
   raise ConfigException("Invalid config role: must be either 'peer' or 'authenticator'. Exiting...")
  gmJBRrAckW['debug']=gmJBRrAckj("Display debug information (true or false): ").lower()
  if(gmJBRrAckW['debug']=='true'):
   gmJBRrAckW['debug']=1
  elif(gmJBRrAckW['debug']=='false'):
   gmJBRrAckW['debug']=0
  else:
   raise ConfigException("Invalid value: must be either 'true' or 'false'. Exiting...")
  try:
   gmJBRrAckW['chunk_size']=int(gmJBRrAckj("Size of the packet chunk to send (e.g., {}): ".format(gmJBRrAcki)))
   if(gmJBRrAckW['chunk_size']<1):
    raise ValueError
  except ValueError:
   raise ConfigException("Invalid value: must be positive integer value. Exiting...")
  for gmJBRrAckY in gmJBRrAckW:
   if(gmJBRrAckW[gmJBRrAckY]==''):
    raise ConfigException('Cannot continue: One or more settings are empty. Exiting...')
 except(ConfigException,EOFError)as err:
  if(isinstance(err,ConfigException)):
   print(err)
  elif(isinstance(err,EOFError)):
   print("\nCannot continue: End of File detected. Exiting...")
  gmJBRrAcFI()
 return gmJBRrAckW
def gmJBRrAcko():
 gmJBRrAckU={'peer':('role','authenticator','port','identity','secret','localname'),'authenticator':('role','port','localname')}
 if(len(gmJBRrAcFd)<2):
  return gmJBRrAckh()
 gmJBRrAckW={}
 try:
  gmJBRrAckW['debug']=0
  gmJBRrAckW['chunk_size']=gmJBRrAcki
  gmJBRrAckW['role']='peer'
  options,arguments=gmJBRrAcFE(gmJBRrAcFd[1:],'r:a:p:i:s:l:c:dh',['role=','authenticator=','port=','identity=','secret=','localname=','chunk=','debug','list-identities','help'])
  for gmJBRrAckG,arg in options:
   if gmJBRrAckG in('-r','--role'):
    if(arg=='peer'):
     gmJBRrAckW['role']='peer'
    elif(arg=='authenticator'):
     gmJBRrAckW['role']='authenticator'
    else:
     raise ConfigException("Invalid config role: "+"must be either 'peer' or 'authenticator'. Exiting...")
   if gmJBRrAckG in('-a','--authenticator'):
    gmJBRrAckW['authenticator']=arg
   if gmJBRrAckG in('-p','--port'):
    gmJBRrAckW['port']=arg
   if gmJBRrAckG in('-i','--identity'):
    gmJBRrAckW['identity']=arg
   if gmJBRrAckG in('-s','--secret'):
    gmJBRrAckW['secret']=arg
   if gmJBRrAckG in('-l','--localname'):
    gmJBRrAckW['localname']=arg
   if gmJBRrAckG in('-c','--chunk'):
    try:
     gmJBRrAckW['chunk_size']=int(arg,10)
     if(gmJBRrAckW['chunk_size']<1):
      raise ConfigException("Invalid chunk size")
    except:
     raise ConfigException("Invalid chunk size")
   if gmJBRrAckG in('-d','--debug'):
    gmJBRrAckW['debug']=1
   if gmJBRrAckG in('--list-identities'):
    gmJBRrAckt()
    gmJBRrAcFI(0)
   if gmJBRrAckG in('-h','--help'):
    gmJBRrAckV()
    gmJBRrAcFI(0)
  for gmJBRrAckY in gmJBRrAckU[gmJBRrAckW['role']]:
   if gmJBRrAckY not in gmJBRrAckW:
    raise ConfigException('Cannot continue: One or more settings are empty. Exiting...')
 except(gmJBRrAcDk,ConfigException)as error:
  print(repr(error))
  gmJBRrAckV()
  gmJBRrAcFI(2)
 return gmJBRrAckW
def gmJBRrAckH():
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Connecting to authenticator {}:{}".format(gmJBRrAcFa['authenticator'],int(gmJBRrAcFa['port'])))
 gmJBRrAcke=gmJBRrAcFy(gmJBRrAcFC,gmJBRrAcFL)
 gmJBRrAcke.connect((gmJBRrAcFa['authenticator'],int(gmJBRrAcFa['port'])))
 gmJBRrAcke.setsockopt(gmJBRrAcFl,gmJBRrAcFT,1)
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Connected!")
 return gmJBRrAcke
def gmJBRrAckO():
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Trying to listen on port {}".format(int(gmJBRrAcFa['port'])))
 gmJBRrAcke=gmJBRrAcFy(gmJBRrAcFC,gmJBRrAcFL)
 gmJBRrAcke.setsockopt(gmJBRrAcFl,gmJBRrAcFT,1)
 gmJBRrAcke.bind(('',int(gmJBRrAcFa['port'])))
 print("Waiting for incoming authentication requests on port "+gmJBRrAcFa['port']+" ...")
 gmJBRrAcke.listen(1)
 conn,addr=gmJBRrAcke.accept()
 return conn
def gmJBRrAckz(gmJBRrAcke,gmJBRrAcFD):
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Trying to send packet with {} octects".format(len(gmJBRrAcFD)))
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Packet chunk size: {} octects".format(gmJBRrAcFa['chunk_size']))
 gmJBRrAckQ=0
 while gmJBRrAckQ<len(gmJBRrAcFD):
  gmJBRrAckI=len(gmJBRrAcFD)-gmJBRrAckQ
  if gmJBRrAckI<gmJBRrAcFa['chunk_size']:
   gmJBRrAckd=gmJBRrAckI
  else:
   gmJBRrAckd=gmJBRrAcFa['chunk_size']
  gmJBRrAcFQ((gmJBRrAcka+(gmJBRrAcFU()*gmJBRrAckf))/1000)
  if(gmJBRrAcFa['debug']):
   gmJBRrAckD("Sending {} octects".format(gmJBRrAckd))
  gmJBRrAckn=gmJBRrAcke.send(gmJBRrAcFD[gmJBRrAckQ:gmJBRrAckQ+gmJBRrAckd])
  if gmJBRrAckn==0:
   raise RuntimeError("socket connection broken")
  gmJBRrAckQ=gmJBRrAckQ+gmJBRrAckn
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Sent {} octects!".format(gmJBRrAckQ))
def gmJBRrAckv(gmJBRrAcke):
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Trying to receive packet header ({} octects)".format(gmJBRrAcku))
 gmJBRrAckE=bytearray()
 while len(gmJBRrAckE)<gmJBRrAcku:
  gmJBRrAcFk=gmJBRrAcke.recv(gmJBRrAcku-len(gmJBRrAckE))
  if gmJBRrAcFk=='':
   raise RuntimeError("socket connection broken")
  if(gmJBRrAcFa['debug']):
   gmJBRrAckD("Received {} octects!".format(len(gmJBRrAcFk)))
  gmJBRrAckE=gmJBRrAckE+gmJBRrAcFk
 gmJBRrAcFD=gmJBRrAckE
 gmJBRrAcFi,gmJBRrAcFh,length=gmJBRrAcFW('!BBH',gmJBRrAckE)
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Trying to receive packet data ({} octects)".format(length-gmJBRrAcku))
 while len(gmJBRrAcFD)<length:
  gmJBRrAcFk=gmJBRrAcke.recv(length-len(gmJBRrAcFD))
  if gmJBRrAcFk=='':
   raise RuntimeError("socket connection broken")
  gmJBRrAcFD=gmJBRrAcFD+gmJBRrAcFk
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Received {} octects!".format(len(gmJBRrAcFD)-gmJBRrAcku))
 gmJBRrAcFi,gmJBRrAcFh,length,gmJBRrAcFv=gmJBRrAcFW('!BBH'+str(length-gmJBRrAcku)+'s',gmJBRrAcFD)
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Header Code: {}, Identifier: {}, Length: {}, Data (hex): {} ".format(gmJBRrAcFi,gmJBRrAcFh,length,gmJBRrAckF(gmJBRrAcFv)))
 return{'code':gmJBRrAcFi,'identifier':gmJBRrAcFh,'length':length,'data':gmJBRrAcFv}
def gmJBRrAckS(gmJBRrAcFi,gmJBRrAcFh,gmJBRrAcFv):
 gmJBRrAcFt=len(gmJBRrAcFv)
 gmJBRrAcFV=gmJBRrAcku+gmJBRrAcFt
 gmJBRrAcFj='!BBH'+str(gmJBRrAcFt)+'s'
 gmJBRrAcFD=gmJBRrAcFY(gmJBRrAcFj,gmJBRrAcFi,gmJBRrAcFh,gmJBRrAcFV,gmJBRrAcFv)
 return gmJBRrAcFD
def gmJBRrAckM():
 print("Creating authentication request for identity:",gmJBRrAcFa['identity'])
 return gmJBRrAckS(gmJBRrAckK,0x00,gmJBRrAcFa['identity'].encode('utf-8'))
def gmJBRrAckb(auth_request_packet):
 gmJBRrAckT=auth_request_packet['data']
 try:
  gmJBRrAckT=gmJBRrAckT.decode('utf-8')
 except UnicodeError:
  gmJBRrAckT=''
 print("Processing authentication request for identity:",gmJBRrAckT)
 return{'identifier':auth_request_packet['identifier'],'identity':gmJBRrAckT}
def gmJBRrAckq():
 gmJBRrAcFh=gmJBRrAcFG(0,255)
 print("Creating challenge with identifier:",gmJBRrAcFh)
 gmJBRrAcFo=gmJBRrAcFf(bytearray(gmJBRrAcFe(range(256),256)))
 gmJBRrAcFH=gmJBRrAcFo.digest()
 gmJBRrAcFO=gmJBRrAcFY('!B',len(gmJBRrAcFH))
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Challenge value size: {}".format(len(gmJBRrAcFH)))
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Challenge value (in hex): {}".format(gmJBRrAckF(gmJBRrAcFH)))
 gmJBRrAcFz=gmJBRrAcFa['localname'].encode('utf-8')
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Name value: {}".format(gmJBRrAcFz))
 gmJBRrAcFv=gmJBRrAcFO+gmJBRrAcFH+gmJBRrAcFz
 gmJBRrAcFD=gmJBRrAckS(gmJBRrAcky,gmJBRrAcFh,gmJBRrAcFv)
 return(gmJBRrAcFD,gmJBRrAcFh,gmJBRrAcFH)
def gmJBRrAckP(challenge_packet):
 gmJBRrAcFS=challenge_packet['data'][0]
 gmJBRrAcFM=challenge_packet['data'][1:gmJBRrAcFS+1]
 gmJBRrAcFz=challenge_packet['data'][gmJBRrAcFS+1:]
 try:
  gmJBRrAcFz=gmJBRrAcFz.decode('utf-8')
 except UnicodeError:
  gmJBRrAcFz=''
 print("Processing challenge with identifier:",challenge_packet['identifier'],", name:",gmJBRrAcFz)
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Challenge value (in hex): {}".format(gmJBRrAckF(gmJBRrAcFM)))
  gmJBRrAckD("Name value: {}".format(gmJBRrAcFz))
 return{'identifier':challenge_packet['identifier'],'challenge':gmJBRrAcFM,'name':gmJBRrAcFz}
def gmJBRrAckx(gmJBRrAcFM):
 print("Creating response with identifier:",gmJBRrAcFM['identifier'])
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Secret value: {}".format(gmJBRrAcFa['secret']))
  gmJBRrAckD("Challenge value (in hex): {}".format(gmJBRrAckF(gmJBRrAcFM['challenge'])))
 gmJBRrAcFo=gmJBRrAcFf(gmJBRrAcFY("!B",gmJBRrAcFM['identifier'])+gmJBRrAcFa['secret'].encode('utf-8')+gmJBRrAcFM['challenge'])
 gmJBRrAcFb=gmJBRrAcFo.digest()
 gmJBRrAcFq=gmJBRrAcFY('!B',len(gmJBRrAcFb))
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Response value (in hex): {}".format(gmJBRrAckF(gmJBRrAcFb)))
 gmJBRrAcFz=gmJBRrAcFa['localname'].encode('utf-8')
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Name value: {}".format(gmJBRrAcFz))
 gmJBRrAcFv=gmJBRrAcFq+gmJBRrAcFb+gmJBRrAcFz
 return gmJBRrAckS(gmJBRrAckC,gmJBRrAcFM['identifier'],gmJBRrAcFv)
def gmJBRrAckw(response_packet):
 gmJBRrAcFP=response_packet['data'][0]
 gmJBRrAcFx=response_packet['data'][1:gmJBRrAcFP+1]
 gmJBRrAcFz=response_packet['data'][gmJBRrAcFP+1:]
 try:
  gmJBRrAcFz=gmJBRrAcFz.decode('utf-8')
 except UnicodeError:
  gmJBRrAcFz=''
 print("Processing response with identifier:",response_packet['identifier'],", name:",gmJBRrAcFz)
 if(gmJBRrAcFa['debug']):
  gmJBRrAckD("Response data (in hex): {}".format(gmJBRrAckF(gmJBRrAcFx)))
 return{'identifier':response_packet['identifier'],'response':gmJBRrAcFx,'name':gmJBRrAcFz}
def gmJBRrAcks(gmJBRrAcFu,gmJBRrAckT,gmJBRrAcFh,gmJBRrAcFM):
 print("Verifying response for identifier:",gmJBRrAcFh)
 if(gmJBRrAckT in gmJBRrAckp):
  if(gmJBRrAcFa['debug']):
   gmJBRrAckD("Processing identity: {}".format(gmJBRrAckT))
  gmJBRrAcFw=gmJBRrAckp[gmJBRrAckT]
  if(gmJBRrAcFa['debug']):
   gmJBRrAckD("Secret for identity: {}".format(gmJBRrAcFw))
  gmJBRrAcFo=gmJBRrAcFf(gmJBRrAcFY("!B",gmJBRrAcFh)+gmJBRrAcFw.encode('utf-8')+gmJBRrAcFM)
  gmJBRrAcFs=gmJBRrAcFo.digest()
  if(gmJBRrAcFa['debug']):
   gmJBRrAckD("Calculated SHA-256 value (in hex): {}".format(gmJBRrAckF(gmJBRrAcFs)))
   gmJBRrAckD("Received SHA-256 value (in hex):   {}".format(gmJBRrAckF(gmJBRrAcFu['response'])))
  if(gmJBRrAcFK(gmJBRrAcFs,gmJBRrAcFu['response'])):
   if(gmJBRrAcFa['debug']):
    gmJBRrAckD("Identity successfully authenticated!")
   return 1
  else:
   if(gmJBRrAcFa['debug']):
    gmJBRrAckD("Identity not authenticated!")
   return 0
 else:
  if(gmJBRrAcFa['debug']):
   gmJBRrAckD("Identity not found: {}".format(gmJBRrAckT))
  return 0
def gmJBRrAckN():
 gmJBRrAcke=gmJBRrAckH()
 gmJBRrAcFD=gmJBRrAckM()
 gmJBRrAckz(gmJBRrAcke,gmJBRrAcFD)
 gmJBRrAcFD=gmJBRrAckv(gmJBRrAcke)
 if(gmJBRrAcFD['code']==gmJBRrAcky):
  gmJBRrAcFN=gmJBRrAckP(gmJBRrAcFD)
  gmJBRrAcFD=gmJBRrAckx(gmJBRrAcFN)
  gmJBRrAckz(gmJBRrAcke,gmJBRrAcFD)
  print("Waiting for Success/Failure packet...")
  gmJBRrAcFD=gmJBRrAckv(gmJBRrAcke)
  if(gmJBRrAcFD['identifier']==gmJBRrAcFN['identifier']):
   if(gmJBRrAcFD['code']==gmJBRrAckL):
    print("Successfully authenticated!")
   elif((gmJBRrAcFD['code']==gmJBRrAckl)):
    print("Could not authenticate. Reason from the authenticator:",gmJBRrAcFD['data'])
   else:
    print("Protocol error")
  else:
   print("Discarding mismatched response packet...")
 else:
  print("Protocol error")
 gmJBRrAcke.close()
def gmJBRrAckX():
 print("\nAvailable identities and secrets to perform the test:\n")
 print("+----------------------------------------+")
 print("| {:<20} | {:<15} |".format("identity","secret"))
 print("+----------------------------------------+")
 for gmJBRrAcFX,password in sorted(gmJBRrAckp.items()):
  print("| {:<20} | {:<15} |".format(gmJBRrAcFX,password))
 print("+----------------------------------------+\n\n")
 gmJBRrAcke=gmJBRrAckO()
 gmJBRrAcFD=gmJBRrAckv(gmJBRrAcke)
 if(gmJBRrAcFD['code']==gmJBRrAckK):
  gmJBRrAcFp=gmJBRrAckb(gmJBRrAcFD)
  gmJBRrAcFD,challenge_identifier,gmJBRrAcFM=gmJBRrAckq()
  gmJBRrAckz(gmJBRrAcke,gmJBRrAcFD)
  gmJBRrAcFD=gmJBRrAckv(gmJBRrAcke)
  if(gmJBRrAcFD['code']==gmJBRrAckC):
   if(gmJBRrAcFD['identifier']==challenge_identifier):
    gmJBRrAcFu=gmJBRrAckw(gmJBRrAcFD)
    if(gmJBRrAcks(gmJBRrAcFu,gmJBRrAcFp['identity'],challenge_identifier,gmJBRrAcFM)):
     gmJBRrAcFi=gmJBRrAckL
     gmJBRrAcFv=''
    else:
     gmJBRrAcFi=gmJBRrAckl
     gmJBRrAcFv='Identity or secret is incorrect'
    gmJBRrAcFD=gmJBRrAckS(gmJBRrAcFi,gmJBRrAcFD['identifier'],gmJBRrAcFv.encode('utf-8'))
    gmJBRrAckz(gmJBRrAcke,gmJBRrAcFD)
   else:
    print("Discarding mismatched response packet...")
  else:
   print("Protocol error")
 else:
  print("Protocol error")
 gmJBRrAcFQ(1)
 gmJBRrAcke.close()
if __name__=="__main__":
 if gmJBRrAcFn.major<3:
  raise BaseException("This program must be run with Python 3.x")
 gmJBRrAcFa=gmJBRrAcko()
 if(gmJBRrAcFa['role']=='peer'):
  gmJBRrAckN()
 elif(gmJBRrAcFa['role']=='authenticator'):
  gmJBRrAckX()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
