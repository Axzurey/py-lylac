from data.tower import TowerInformation
import lylac


class TowerWidget:
    towerInfo: list[TowerInformation]
    def __init__(self, display: lylac.Instance, towerInfo: list[TowerInformation]) -> None:
        self.towerInfos = towerInfo;

        frame = lylac.Frame();
        frame.zIndex = 999;
        frame.parent = display;
        frame.cornerRadius = 45;
        frame.size = lylac.Udim2.fromOffset(400, 150)
        frame.onMouseButton1Down.connect(lambda _: print('c'))