package data

import "log"

type DataPatch interface {
	Row() int
	Column() int
	Number() int
	ToLog() string
}

type SudokuDataController struct {
	Sudoku
	countNumberCache [10]int //количество каждой цифры в судоку
	countCellVar     [81]int //количество элементов которые можно разместить в ячейку
	// имеют значение true если туда можно поставить цифру
	rowsCache              [9][10]bool      //кеш строк
	columnsCache           [9][10]bool      //кеш столбцов
	squareCache            [9][10]bool      //кеш квадратов
	positionsOfNumberCache [10]map[int]bool //кеш позиций для цифры 0-81
}

func NewSudokuDataController(su Sudoku) *SudokuDataController {
	sdc := new(SudokuDataController)
	sdc.Sudoku = su
	sdc.init()
	return sdc
}
func (sdc *SudokuDataController) GetFreePositionForNumber(num int) map[int]bool {
	return sdc.positionsOfNumberCache[num]
}
func (sdc *SudokuDataController) GetCountNumber() []int {
	return sdc.countNumberCache[:]
}
func (sdc *SudokuDataController) GetCountCell() []int {
	return sdc.countCellVar[:]
}
func (sdc *SudokuDataController) CalculateEfficiency(patch DataPatch) int {
	return sdc.calculateEfficiency(patch.Row(), patch.Column(), patch.Number())
}
func (sdc *SudokuDataController) calculateEfficiency(row, col, num int) int {
	var res int = 0
	for i := 0; i < 9; i++ {
		if i != ((row/3)*3 + i/3) {
			if _, ok := sdc.positionsOfNumberCache[num][i*9+col]; ok {
				res++
			}
		}
		if i != ((col/3)*3 + i%3) {
			if _, ok := sdc.positionsOfNumberCache[num][row*9+i]; ok {
				res++
			}
		}
		if _, ok := sdc.positionsOfNumberCache[num][((row/3)*3+i/3)*9+((col/3)*3+i%3)]; ok {
			res++
		}
		if i+1 != num {
			if _, ok := sdc.positionsOfNumberCache[i+1][row*9+col]; ok {
				res++
			}
		}
	}
	return res
}
func (sdc *SudokuDataController) Load(s string) {
	sdc.LoadFromHashStr(s)
	sdc.init()
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
		sdc.countNumberCache[num] = 0
	}
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			sdc.rowsCache[row][sdc.field[row][col]] = false
			sdc.columnsCache[col][sdc.field[row][col]] = false
			sdc.squareCache[(row/3)*3+col/3][sdc.field[row][col]] = false
			sdc.countNumberCache[sdc.field[row][col]]++
			sdc.countCellVar[row*9+col] = 0
		}
	}
	// находится здесь а не перенесен в верхнии циклы потому что требуется предварительный просчет других кешей
	//требуется для вызова функции IsPossibleInstall
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			for num := 1; num < 10; num++ {
				if sdc.IsPossibleInstall(row, col, num) {
					sdc.positionsOfNumberCache[num][row*9+col] = true
					sdc.countCellVar[row*9+col]++
				}
			}
		}
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
			if _, ok := sdc.positionsOfNumberCache[num][i*9+col]; ok {
				delete(sdc.positionsOfNumberCache[num], i*9+col)
				sdc.countCellVar[i*9+col]--
			}
		}
		if i != ((col/3)*3 + i%3) {
			if _, ok := sdc.positionsOfNumberCache[num][row*9+i]; ok {
				delete(sdc.positionsOfNumberCache[num], row*9+i)
				sdc.countCellVar[row*9+i]--
			}
		}
		if _, ok := sdc.positionsOfNumberCache[num][((row/3)*3+i/3)*9+((col/3)*3+i%3)]; ok {
			delete(sdc.positionsOfNumberCache[num], ((row/3)*3+i/3)*9+((col/3)*3+i%3))
			sdc.countCellVar[((row/3)*3+i/3)*9+((col/3)*3+i%3)]--
		}
		if i+1 != num {
			if _, ok := sdc.positionsOfNumberCache[i+1][row*9+col]; ok {
				delete(sdc.positionsOfNumberCache[i+1], row*9+col)
				sdc.countCellVar[row*9+col]--
			}
		}
	}
	sdc.countNumberCache[num]++
	sdc.countNumberCache[0]--
}
func (sdc *SudokuDataController) Set(patch DataPatch) {
	log.Println("set", patch.ToLog())
	log.Println(sdc.field)
	log.Println(sdc.rowsCache)
	log.Println(sdc.columnsCache)
	log.Println(sdc.squareCache)
	log.Println(sdc.positionsOfNumberCache)
	log.Println(sdc.countCellVar)
	log.Println(sdc.countNumberCache)
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
			sdc.countCellVar[i*9+col]++
		}
		if i != ((col/3)*3+i%3) && sdc.IsPossibleInstall(row, i, num) {
			sdc.positionsOfNumberCache[num][row*9+i] = true
			sdc.countCellVar[row*9+i]++
		}
		if sdc.IsPossibleInstall((row/3)*3+i/3, (col/3)*3+i%3, num) {
			sdc.positionsOfNumberCache[num][((row/3)*3+i/3)*9+((col/3)*3+i%3)] = true
			sdc.countCellVar[((row/3)*3+i/3)*9+((col/3)*3+i%3)]++
		}
		if i+1 != num && sdc.IsPossibleInstall(row, col, i+1) {
			sdc.positionsOfNumberCache[i+1][row*9+col] = true
			sdc.countCellVar[row*9+col]++
		}
	}
	sdc.countNumberCache[num]--
	sdc.countNumberCache[0]++
}
func (sdc *SudokuDataController) Unset(patch DataPatch) {
	log.Println("unset", patch.ToLog())
	log.Println(sdc.field)
	log.Println(sdc.rowsCache)
	log.Println(sdc.columnsCache)
	log.Println(sdc.squareCache)
	log.Println(sdc.positionsOfNumberCache)
	log.Println(sdc.countCellVar)
	log.Println(sdc.countNumberCache)
	sdc.unset(patch.Row(), patch.Column(), patch.Number())
}
func (sdc *SudokuDataController) IsSolved() bool {
	if sdc.countNumberCache[0] == 0 {
		return true
	}
	return false
}
