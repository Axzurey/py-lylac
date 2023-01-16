from typing import Any;
import lylac;

class signalBin:
    connections: list[lylac.LylacConnection];

    def __init__(self) -> None:
        self.connections = [];

    def add(self, conn: lylac.LylacConnection):
        self.connections.append(conn);

    def drop(self):
        for connection in self.connections:
            connection.disconnect();

def useSignalBin():
    return signalBin();