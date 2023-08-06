# kanjigrid
Create Kanji Grids out of Text

```python
pip install kanjigrid
```

##  MWE
```python
import kanjigrid

gridder = kanjigrid.Gridder("Kanji", 40, "Header", 52)
grading = kanjigrid.Jouyou()

with open("test.txt", "r", encoding="utf-8") as f:
    data = f.read()

gridder.feed_text(data)
grid = gridder.make_grid(grading, outside_of_grading=True, stats=True, bar_graph=True)
grid.save("test.png")
```

![](https://github.com/exc4l/kanjigrid/blob/main/test.png)
