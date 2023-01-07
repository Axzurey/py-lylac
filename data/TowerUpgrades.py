from __future__ import annotations;
from typing import Optional, Type;

class TowerUpgrade:
    name: str;
    description: str;
    requires: Optional[Type[TowerUpgrade]];

class IncreaseFirepowerI(TowerUpgrade):
    name = "Increase Firepower I";
    description = "Slightly increase the tower's attack.";
    
class IncreaseFirepowerII(TowerUpgrade):
    name = "Increase Firepower II";
    description = "Generously Increase the tower's attack.";
    requires = IncreaseFirepowerI;

class IncreaseFirepowerIII(TowerUpgrade):
    name = "Increase Firepower III";
    description = "Greatly increase the tower's attack.";
    requires = IncreaseFirepowerII;

class IncreaseFirepowerIV(TowerUpgrade):
    name = "Increase Firepower IV";
    description = "Massively Increase the tower's attack.";
    requires = IncreaseFirepowerIII;

class IncreaseFirepowerV(TowerUpgrade):
    name = "Increase Firepower V";
    description = "Exponentially increase the tower's attack.";
    requires = IncreaseFirepowerIV;

class BoostClockSpeedI(TowerUpgrade):
    name = "Boost Clock Speed I";
    description = "Slightly increase the tower's rate of fire.";

class BoostClockSpeedII(TowerUpgrade):
    name = "Boost Clock Speed II";
    description = "Generously Increase the tower's rate of fire.";
    requires = BoostClockSpeedI;

class BoostClockSpeedIII(TowerUpgrade):
    name = "Boost Clock Speed III";
    description = "Greatly increase the tower's rate of fire.";
    requires = BoostClockSpeedII;

class BoostClockSpeedIV(TowerUpgrade):
    name = "Boost Clock Speed IV";
    description = "Massively increase the tower's rate of fire.";
    requires = BoostClockSpeedIII;

class BoostClockSpeedV(TowerUpgrade):
    name = "Boost Clock Speed V";
    description = "Exponentially increase the tower's rate of fire.";
    requires = BoostClockSpeedIV;