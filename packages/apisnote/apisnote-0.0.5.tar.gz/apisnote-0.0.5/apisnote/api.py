import requests


class Note:
	def __init__(self, apikey: str, lang: str = "en") -> None:
		if len(apikey) != 32:
			raise RuntimeError("api key length must be 32")
		self.lang = lang
		self.apikey = apikey
		self.url = "https://apis.kgbot.pp.ua/api/{0}?apikey={1}&lang={2}"
	
	
	def _get(self, method: str, **kwargs) -> dict:
		r = requests.get(self.url.format(method, self.apikey, self.lang), params=kwargs)
		return r.json()
		
	
	def addNote(self, name: str, content: str) -> dict:
		"""Метод для добавления заметок
		```name``` - имя заметки
		```content``` - содержимое заметки
		"""
		return self._get("addNote", name=name, content=content)
	
	
	def getNote(self, name: str) -> dict:
		"""Метод для получения заметки
		```name``` - имя заметки
		"""
		return self._get("getNote", name=name)
	
	
	def getNoteList(self) -> dict:
		"""Метод для получения всех заметок"""
		return self._get("getNoteList")
	
	
	def removeNote(self, name: str) -> dict:
		"""Метод для удаления заметки
		```name``` - имя заметки
		"""
		return self._get("removeNote", name=name)
	
	
	def editNote(self, name: str, content: str) -> dict:
		"""Метод для редактирования заметки
		```name``` - имя заметки
		```content``` - новое содержимое заметки
		"""
		return self._get("editNote", name=name, content=content)
	

	def __str__(self):
		return f"<Note apikey=\"{self.apikey}\">"
