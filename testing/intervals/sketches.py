%load_ext autoreload
autoreload 2
from spartan.utils.annotations import intervals as i
intervals = []
intervals.append(i.Interval(1, 9,1))
intervals.append(i.Interval(5, 6,1))
intervals.append(i.Interval(12, 14,1))
intervals.append(i.Interval(14, 15,1))
intervals.append(i.Interval(17, 20,1))
intervals.append(i.Interval(21, 25,1))
intervals.append(i.Interval(27, 33,1))
intervals
a,b,c,d,e,f,g = intervals
a.grow(3)


repr(a)
str(a)
a in b # False
b in a # True
#'this' in a # fail
merged = list(a.merge(intervals))








a < b
b < a
a <= b
b <= a
a == b
b == a
a == a
a is a
1 in a
a.overlaps(b)
b.overlaps(a)
c in d
d in c
d.overlaps(c)
e in f
e.overlaps(f)
e.grow(1)
e.grow(1).overlaps(f)


