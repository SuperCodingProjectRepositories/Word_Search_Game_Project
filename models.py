from typing import Annotated,List
from pydantic import BaseModel

class GameData(BaseModel):
    title: str
    description: str
    words: List[str]
    public: bool

class Game(BaseModel):
    title: str = ""
    description: str = ""
    words: List[str] = []
    matched_words: List[str] = []
    is_completed: bool = False

    def check_word(self, word: str) -> bool:
        """단어가 맞으면 True 반환하고 matched_words에 추가"""
        if word in self.words and word not in self.matched_words:
            self.matched_words.append(word)
            self.is_completed = self.is_game_complete()
            return True
        return False

    def is_game_complete(self) -> bool:
        """모든 단어를 맞췄는지 확인"""
        return set(self.matched_words) == set(self.words)
