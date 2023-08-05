from osisunderwayconnector import OsisUnderwayConnector, OsisUnderwayConnectorError

import mariqt.geo as miqtg
import mariqt.files as miqtf
import mariqt.variables as miqtv
import mariqt.navigation as miqtn

import json
import yaml
import datetime

# TODO: iFDO Connector


def uploadEventListToUnderway(csv_path:str,platform:str,user:str,api_url:str = miqtv.apis['osis_underway']):

	positions = miqtn.readAllPositionsFromFilePath(csv_path,{'utc':'Date Time','lon':'Longitude','lat':'Latitude','dep':'Depth'},miqtv.date_formats['dship'])
	tmp_events = miqtf.tabFileData(csv_path,['Date Time','Event'],key_col = 'Date Time')

	events = {}
	for e in tmp_events:
		dt = datetime.datetime.strptime(e+"+0000",miqtv.date_formats['dship']+"%z")
		events[int(dt.timestamp())] = tmp_events[e]['Event']

	con = MarIQTConnector(api_url,platform,user,'MarIQTEvents')

	con.set_positions(positions,events)
	con.do_import()


class MarIQTConnector(OsisUnderwayConnector):

	""" Connects the mariqt positions world to the OSIS underway positions world.

		Create an instance of this class and provide it with the API URL (ask cfaber for one if you do not know it) and
		a platform (shortname) for the gear you are adding positions for (again, ask cfaber ... ).
		Then get your positions ready in a mariqt.geo.Positions format.
		If you want to add payload to the data (underway-speech for e.g. parameters like temperature at a position,
		or a station name) then you also need to provide this as a list of equal size as the Positions list.
		Once you have the instance of this object created, run its *do_import* method to do the magic!"""

	def __init__(self, api_url:str, platform:str, contact:str, stream:str = "MarIQT"):
		super().__init__(api_url)
		self.platform = platform
		self.contact = contact
		self.stream = stream
		self.positions = []

	@property
	def datastream(self):
		return self.stream
	
	@property
	def contact_person(self):
		return self.contact
	
	def get_positions(self):
		return self.positions

	def set_positions(self, positions:miqtg.Positions, payloads:list = []):
		use_payload = False

		if len(payloads) > 0 and len(payloads) != positions.len():
			raise OsisUnderwayConnectorError("Positions and payload lengths do not match!")
		else:
			use_payload = True

		self.positions = []

		for utc in positions.positions:

			pos = positions.positions[utc]

			# Get the time in the correct format
			utc_str = datetime.datetime.fromtimestamp(pos.utc,tz=datetime.timezone.utc).strftime(miqtv.date_formats['underway'])

			if use_payload:
				payload = payloads[utc]
				self.positions.append({'latitude':pos.lat, 'longitude':pos.lon, 'obs_timestamp':utc_str, 'platform':self.platform, 'payload': {'data': {'event':payload},'data_format': "string"}})
			else:
				self.positions.append({'latitude':pos.lat, 'longitude':pos.lon, 'obs_timestamp':utc_str, 'platform':self.platform})
