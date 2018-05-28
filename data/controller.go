package data

type Controller struct {
	Sudoku
	countNumberCache [10]int //количество каждой цифры в судоку
	// имеют значение true если туда можно поставить цифру
	rowsCache    [9][10]bool //кеш строк
	columnsCache [9][10]bool //кеш столбцов
	squareCache  [9][10]bool //кеш квадратов
}

func (c *Controller) Load(s string) {
	c.LoadFromHashStr(s)
	c.init()
}
func (c *Controller) GetCountNumber() []int {
	return c.countNumberCache[:]
}
func (c *Controller) init() {
	for i := 0; i < 9; i++ {
		for num := 0; num < 10; num++ {
			c.rowsCache[i][num] = true
			c.columnsCache[i][num] = true
			c.squareCache[i][num] = true
		}
	}
	for num := 0; num < 10; num++ {
		c.countNumberCache[num] = 0
	}
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			c.rowsCache[row][c.field[row][col]] = false
			c.columnsCache[col][c.field[row][col]] = false
			c.squareCache[(row/3)*3+col/3][c.field[row][col]] = false
			c.countNumberCache[c.field[row][col]]++
		}
	}
}
func (c *Controller) IsPossibleInstall(row, col, num int) bool {
	if c.field[row][col] != 0 {
		return false
	}
	var res bool = c.rowsCache[row][num]
	res = res && c.columnsCache[col][num]
	res = res && c.squareCache[(row/3)*3+col/3][num]
	return res
}
func (c *Controller) set(row, col, num int) {
	c.field[row][col] = num
	c.rowsCache[row][num] = false
	c.columnsCache[col][num] = false
	c.squareCache[(row/3)*3+col/3][num] = false
	c.countNumberCache[num]++
	c.countNumberCache[0]--
}
func (c *Controller) Set(patch *Patch) {
	c.set(patch.Row(), patch.Column(), patch.Number())
}
func (c *Controller) unset(row, col, num int) {
	c.field[row][col] = 0
	c.rowsCache[row][num] = true
	c.columnsCache[col][num] = true
	c.squareCache[(row/3)*3+col/3][num] = true
	c.countNumberCache[num]--
	c.countNumberCache[0]++
}
func (c *Controller) Unset(patch *Patch) {
	c.unset(patch.Row(), patch.Column(), patch.Number())
}
func (c *Controller) IsSolved() bool {
	if c.countNumberCache[0] == 0 {
		return true
	}
	return false
}
func (c *Controller) GetMinCountOfRemainingNumber() int {
	num := -1
	val := -1
	for ind, v := range c.countNumberCache {
		if ind == 0 {
			continue
		}
		if v < 9 && v > val {
			num = ind
			val = v
		}
	}
	return num
}
func (c *Controller) GetPossibleCellForNumber(num int) []int {
	res := make([]int, 0)
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			if c.IsPossibleInstall(row, col, num) {
				res = append(res, row*9+col)
			}
		}
	}
	return res
}
