from musicbrainz_api_request import apiRequestor
from music_object_class import MusicObject

class Main:

	def main(self) -> None:
		print(u'------------++++++++MU$IC F1NDER+++++++-----------')
		print(u'Find the average word count for any music artist.\n')
		artist_id = None 
		full_track_list = []
		lyrics = [] 
		text = 'Please enter an artist name:\n'
		music_object = MusicObject(artist_id, full_track_list, lyrics, text)
		apirequestor = apiRequestor()
		apirequestor.assign_useragent()
		apirequestor.retrieve_artist_details(music_object)
		apirequestor.retrieve_release_details(music_object)
		print(music_object.full_track_list)
	
	def run(self) -> None:
		self.main()
		
if __name__ == "__main__":
    Main().run()