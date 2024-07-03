from database.DB_connect import DBConnect
from modello.album import Album


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getAlbumNodes(durataMin):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.* , sum(t.Milliseconds)/60000 as DurataAlbum 
                    from itunes.album a , itunes.track t 
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId 
                    having sum(t.Milliseconds)/60000 > %s
                    """

        cursor.execute(query, (durataMin, ))

        for row in cursor:
            result.append(Album(row["AlbumId"],
                                row["Title"],
                                row["ArtistId"],
                                row["DurataAlbum"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinctrow t.AlbumId as a1, t2.AlbumId as a2
                    from itunes.playlisttrack p , itunes.track t , itunes.playlisttrack p2, itunes.track t2
                    where p2.PlaylistId = p.PlaylistId
                    and p2.TrackId = t2.TrackId 
                    and p.TrackId = t.TrackId
                    and t.AlbumId < t2.AlbumId
                 """

        cursor.execute(query)

        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append((idMap[row["a1"]], idMap[row["a2"]]))
        cursor.close()
        conn.close()
        return result
