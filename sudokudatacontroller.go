package main

import ()

type SudokuDataController struct {
	*Sudoku
	countNumberCache [10]int //количество каждой цифры в судоку
	// имеют значение true если туда можно поставить цифру
	rowsCache    [9][10]bool    //кеш строк
	columnsCache [9][10]bool    //кеш столбцов
	squareCache  [9][10]bool    //кеш квадратов
	cubeCache    [9][9][10]bool //кеш ячейки
}

func NewCacheController(su *Sudoku) *SudokuDataController {
	sdc := new(SudokuDataController)
	sdc.init()
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			sdc.rowsCache[row][su.field[row][col]] = false
			sdc.columnsCache[col][su.field[row][col]] = false
			sdc.squareCache[(row/3)*3+col/3][su.field[row][col]] = false
		}
	}
	// находится здесь а не перенесен в верхнии циклы потому что требуется предварительный просчет других кешей
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			for num := 0; num < 10; num++ {
				sdc.cubeCache[row][col][num] = sdc.IsPossibleInstall(row, col, num)
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
			for j := 0; j < 9; j++ {
				sdc.cubeCache[i][j][num] = true
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
		if sdc.cubeCache[i][col][num] {
			sdc.cubeCache[i][col][num] = false
		}
		if sdc.cubeCache[row][i][num] {
			sdc.cubeCache[row][i][num] = false
		}
		if sdc.cubeCache[(row/3)*3+i/3][(col/3)*3+i%3][num] {
			sdc.cubeCache[(row/3)*3+i/3][(col/3)*3+i%3][num] = false
		}
	}
	sdc.countNumberCache[num] += 1
	sdc.countNumberCache[0] -= 1
}
func (sdc *SudokuDataController) unset(row, col, num int) {
	sdc.field[row][col] = 0
	sdc.rowsCache[row][num] = true
	sdc.columnsCache[col][num] = true
	sdc.squareCache[(row/3)*3+col/3][num] = true
	for i := 0; i < 9; i++ {
		if sdc.IsPossibleInstall(i, col, num) {
			sdc.cubeCache[i][col][num] = true
		}
		if sdc.IsPossibleInstall(row, i, num) {
			sdc.cubeCache[row][i][num] = true
		}
		if sdc.IsPossibleInstall((row/3)*3+i/3, (col/3)*3+i%3, num) {
			sdc.cubeCache[(row/3)*3+i/3][(col/3)*3+i%3][num] = true
		}
	}
	sdc.countNumberCache[num] -= 1
	sdc.countNumberCache[0] += 1
}
