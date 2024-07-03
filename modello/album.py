from dataclasses import dataclass


@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    durataAlbum: float

    def __hash__(self):
        return hash(self.AlbumId)

    def __str__(self):
        return f"{self.Title} - {self.durataAlbum}"
