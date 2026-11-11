#!/usr/bin/env python3
"""Checks of analyze.py's rules on made-up looks (no study look is read). Run: python3 test_analyze.py"""
from analyze import Decision, flags_of, kinds_named, seen, times_named


def dec(key, kind, start, end, label="bad"):
    rnd, film, rest = key.split("/")
    return Decision({"key": key, "kind": kind, "round": rnd, "film": film, "start_s": start, "end_s": end, "label": label, "case": "Madame_T"})


Z1 = dec("r/f/zoom@8.20", "zoom", "8.2", "9.0")
Z2 = dec("r/f/zoom@19.00", "zoom", "19.0", "19.8")
T1 = dec("r/f/title@4.87", "title", "4.87", "7.87", "good")
Z3 = dec("r/f/zoom@30.00", "zoom", "30.0", "31.0")
Z4 = dec("r/f/zoom@32.00", "zoom", "32.0", "33.0")
FILM = [Z1, Z2, T1, Z3, Z4]


def look(changes=(), verdicts=(), frames=(), titles=()):
    return {"look": {"titles": [{"text": t} for t in titles]}, "frames": list(frames),
            "outcome": {"score": 0.7, "changes": list(changes), "verdicts": list(verdicts)}}


def ch(lo, hi, change, why=""):
    return {"from": lo, "to": hi, "change": change, "why": why}


def test():
    # words name the kind; "punch in" names a zoom; a change names nothing → no flag
    assert kinds_named("Punch in on the boots", [], False) == {"zoom"}
    assert kinds_named("Zoomed too early", [], False) == {"zoom"}
    assert kinds_named("Move the title up", [], False) == {"title"}
    assert kinds_named("Remove the 0.4 s flash", [], False) == set()
    assert kinds_named("caption text larger", [], False) == {"title"}          # "text" names a title, as frozen
    assert kinds_named("the label flashes", [], False) == set()
    assert kinds_named("the label flashes", [], True) == {"title"}             # sensitivity only
    assert kinds_named('Start "With wide trousers" at 3.67 s', ["with wide trousers"], True) == {"title"}
    assert kinds_named('Start "With wide trousers" at 3.67 s', ["with wide trousers"], False) == set()

    # overlap within 0.5 s, nearest decision of that kind, one decision per change
    f = flags_of(look([ch(9.3, 10.0, "Zoom in on the bag")]), FILM)
    assert f == {Z1.key: "flag"}, f
    f = flags_of(look([ch(9.6, 10.0, "Zoom in on the bag")]), FILM)
    assert f == {}, f                                                            # 0.6 s after the zoom ends: no overlap
    f = flags_of(look([ch(5.0, 20.0, "Zoom less")]), FILM)
    assert f == {Z1.key: "flag"} or f == {Z2.key: "flag"} or len(f) == 1, f      # one decision only
    f = flags_of(look([ch(31.0, 32.0, "zoom")]), FILM)
    assert f == {Z3.key: "tie", Z4.key: "tie"}, f                                # equally near: a tie
    f = flags_of(look([ch(31.0, 32.0, "zoom"), ch(32.2, 32.8, "zoom")]), FILM)
    assert f == {Z3.key: "tie", Z4.key: "flag"}, f                               # a flag beats a tie
    f = flags_of(look([ch(5.0, 6.0, "Zoom on the title card")]), FILM)
    assert f == {T1.key: "flag"}, f                                              # names both kinds; only the title overlaps

    # verdicts: a fail whose saw names a time in the window and the kind
    assert times_named("0:00.3–1.5 the title sits at 70% height") == [(0.3, 1.5)]
    assert times_named("0:01.5 white 'Stella Boots'") == [(1.5, 1.5)]
    assert times_named("4.4 s and every look") == [(4.4, 4.4)]
    assert times_named("from 12–13 s") == [(12.0, 13.0)]
    assert times_named("1:05–1:10 zoom") == [(65.0, 70.0)]
    v = {"id": "G-ZOOMS-2", "verdict": "fail", "saw": "the zoom at 0:08.5 lands before the word"}
    assert flags_of(look(verdicts=[v]), FILM) == {Z1.key: "flag"}
    assert flags_of(look(verdicts=[dict(v, verdict="pass")]), FILM) == {}
    assert flags_of(look(verdicts=[dict(v, saw="the pictures at 0:08.5 sit low")]), FILM) == {}

    # seen: a frame inside the decision's own time
    assert seen(look(frames=[8.5]), Z1) and not seen(look(frames=[9.3]), Z1)

    # chance-style shift moves the change away
    assert flags_of(look([ch(9.3, 10.0, "Zoom in")]), FILM, shift=lambda lo, hi: (40.0, 40.7)) == {}
    print("all checks passed")


if __name__ == "__main__":
    test()
