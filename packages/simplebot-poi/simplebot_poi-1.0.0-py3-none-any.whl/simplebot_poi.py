import io

import simplebot
from deltachat import Message
from simplebot.bot import Replies
from staticmap import CircleMarker, StaticMap

__version__ = "1.0.0"


@simplebot.filter
def filter_coordinates(message: Message, replies: Replies) -> None:
    """Detect map coordinates in messages and reply with map picture."""
    if message.text.startswith("geo:"):

        lat, lon = map(float, message.text[4:].split(","))
        m = StaticMap(600, 400, url_template="http://a.tile.osm.org/{z}/{x}/{y}.png")
        m.add_marker(CircleMarker((lon, lat), "white", 18))
        m.add_marker(CircleMarker((lon, lat), "#1d93e4", 12))

        img = m.render()
        fd = io.BytesIO()
        img.save(fd, format="png")
        fd.seek(0)
        replies.add(filename="poi.png", bytefile=fd, quote=message)


class TestPlugin:
    def test_filter(self, mocker):
        msg = mocker.get_one_reply("geo: 46.012022036233546,9.29286152010328")
        assert msg.filename

        msgs = mocker.get_replies("test geo: 46.012022036233546,9.29286152010328")
        assert not msgs
