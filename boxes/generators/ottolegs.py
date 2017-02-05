#!/usr/bin/env python3
# Copyright (C) 2013-2016 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *
from boxes import edges

class LegEdge(edges.BaseEdge):

    def __call__(self, l, **kw):
        d0 = (l - 12.0) /2
        self.hole(l/2, 6, 3.0)
        self.polyline(d0, 90, 0, (-180, 6), 0, 90, d0)

class OttoLegs(Boxes):
    """Otto LC - a laser cut chassis for Otto DIY - legs"""

    ui_group = "Unstable"

    def __init__(self):
        Boxes.__init__(self)

        # Uncomment the settings for the edge types you use
        self.addSettingsArgs(edges.FingerJointSettings)

        # remove cli params you do not need
        #self.buildArgParser("x", "sx", "y", "sy", "h", "hi")
        # Add non default cli params if needed (see argparse std lib)
        #self.argparser.add_argument(
        #    "--XX",  action="store", type=float, default=0.5,
        #    help="DESCRIPTION")

    def foot(self, x, y, ly, l, r=5., move=None):
        if self.move(x, y, move, True):
            return

        t = self.thickness
        w = ly + 5.5 + 2 * t
        self.fingerHolesAt(x/2 - w/2, 0, l, 90)
        self.fingerHolesAt(x/2 + w/2, 0, l, 90)
        self.moveTo(r, 0)

        for l in (x, y, x, y):
            self.polyline(l - 2*r, 45, r*2**0.5, 45)
        
        
        
        self.move(x, y, move)

    def ankle1(self):
        # from vertical edge
        self.hole(15, 10, 2.3) # 3.45 for servo arm
        
    def ankle2(self):
        # from vertical edge
        self.hole(15, 10, 1.5)

    def servoHole(self):
        self.hole(6, 6, 11.6/2)
        self.hole(6, 12, 5.5/2)

    def render(self):
        # adjust to the variables you want in the local scope
        t = self.thickness
        # Initialize canvas
        self.open()

        lx, ly, lh = 12.4, 22.5, 40.0

        self.ctx.save()
        # Legs

        c1 = edges.CompoundEdge(self, "EF", (6.0, lh-6.0))
        e = ["F", c1, "F", "F"]
        self.rectangularWall(lx, lh-6., [LegEdge(self, None), "f", "F", "f"], move="right")
        self.rectangularWall(lx, lh, "FfFf", callback=[
            lambda:self.hole(6, 6, 1.5)], move="right")
        self.rectangularWall(ly, lh, e, move="right")
        self.rectangularWall(ly, lh, e, move="right")
        self.rectangularWall(lx, ly, "Efff", callback=[
            lambda:self.rectangularHole(6.1, 6.35, 12, 2.4), None,
            lambda:self.rectangularHole(4, 8, 8, 2.)], move="right")
        self.rectangularWall(lx, ly, "ffff", callback=[lambda: self.hole(lx/2, ly/2, 2.3)], move="right")
        self.rectangularWall(lx, ly, "eeee", callback=[lambda: self.hole(lx/2, ly/2, 1.5)], move="right")
        self.ctx.restore()
        self.rectangularWall(lx, lh, "ffff", move="up only")

        # feet
        self.rectangularTriangle(30, 25, "fee", r=20, num=4, callback=[None, self.ankle1], move="right")
        self.rectangularTriangle(30, 25, "fee", r=20, num=4, callback=[None, self.ankle2], move="right")
        self.foot(60, 40, ly, 30, move="right")
        self.foot(60, 40, ly, 30, move="right")
        self.close()

def main():
    b = OttoLegs()
    b.parseArgs()
    b.render()

if __name__ == '__main__':
    main()
