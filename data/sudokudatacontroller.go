package data

type DataPatch interface {
	Row() int
	Column() int
	Number() int
}

type SudokuDataController struct {
	*Sudoku
	countNumberCache [10]int //количество каждой цифры в судоку
	// имеют значение true если туда можно поставить цифру
	rowsCache              [9][10]bool      //кеш строк
	columnsCache           [9][10]bool      //кеш столбцов
	squareCache            [9][10]bool      //кеш квадратов
	positionsOfNumberCache [10]map[int]bool //кеш позиций для цифры 0-81
}

func NewSudokuDataController(su *Sudoku) *SudokuDataController {
	sdc := new(SudokuDataController)
	sdc.Sudoku = su
	sdc.init()
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			sdc.rowsCache[row][sdc.field[row][col]] = false
			sdc.columnsCache[col][sdc.field[row][col]] = false
			sdc.squareCache[(row/3)*3+col/3][sdc.field[row][col]] = false
			sdc.countNumberCache[sdc.field[row][col]]++
		}
	}
	// находится здесь а не перенесен в верхнии циклы потому что требуется предварительный просчет других кешей
	//требуется для вызова функции IsPossibleInstall
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			for num := 1; num < 10; num++ {
				if sdc.IsPossibleInstall(row, col, num) {
					sdc.positionsOfNumberCache[num][row*9+col] = true
				}
			}
		}
	}
	return sdc
}

func (sdc *SudokuDataController) init() {
	for i := 0; i < 9; i++ {
		for num := 0; num < 10; num++ {
			sdc.rowsCache[i][num] = true
			sdc.columnsCache[i][num] = true
			sdc.squareCache[i][num] = true
		}
	}
	for num := 0; num < 10; num++ {
		sdc.positionsOfNumberCache[num] = make(map[int]bool)
	}
}
func (sdc *SudokuDataController) IsPossibleInstall(row, col, num int) bool {
	if sdc.field[row][col] != 0 {
		return false
	}
	var res bool = sdc.rowsCache[row][num]
	res = res && sdc.columnsCache[col][num]
	res = res && sdc.squareCache[(row/3)*3+col/3][num]
	return res
}
func (sdc *SudokuDataController) set(row, col, num int) {
	sdc.field[row][col] = num
	sdc.rowsCache[row][num] = false
	sdc.columnsCache[col][num] = false
	sdc.squareCache[(row/3)*3+col/3][num] = false
	for i := 0; i < 9; i++ {
		if i != ((row/3)*3 + i/3) {
			delete(sdc.positionsOfNumberCache[num], i*9+col)
		}
		if i != ((col/3)*3 + i%3) {
			delete(sdc.positionsOfNumberCache[num], row*9+i)
		}
		delete(sdc.positionsOfNumberCache[num], ((row/3)*3+i/3)*9+((col/3)*3+i%3))
	}
	sdc.countNumberCache[num] += 1
	sdc.countNumberCache[0] -= 1
}
func (sdc *SudokuDataController) Set(patch DataPatch) {
	sdc.set(patch.Row(), patch.Column(), patch.Number())
}
func (sdc *SudokuDataController) unset(row, col, num int) {
	sdc.field[row][col] = 0
	sdc.rowsCache[row][num] = true
	sdc.columnsCache[col][num] = true
	sdc.squareCache[(row/3)*3+col/3][num] = true
	for i := 0; i < 9; i++ {
		if i != ((row/3)*3+i/3) && sdc.IsPossibleInstall(i, col, num) {
			sdc.positionsOfNumberCache[num][i*9+col] = true
		}
		if i != ((col/3)*3+i%3) && sdc.IsPossibleInstall(row, i, num) {
			sdc.positionsOfNumberCache[num][row*9+i] = true
		}
		if sdc.IsPossibleInstall((row/3)*3+i/3, (col/3)*3+i%3, num) {
			sdc.positionsOfNumberCache[num][((row/3)*3+i/3)*9+((col/3)*3+i%3)] = true
		}
	}
	sdc.countNumberCache[num] -= 1
	sdc.countNumberCache[0] += 1
}
func (sdc *SudokuDataController) Unset(patch DataPatch) {
	sdc.unset(patch.Row(), patch.Column(), patch.Number())
}
