package strategy

import "sudoku/data"

type Strategy interface {
	Init(sdc *data.SudokuDataController)
	GetResult() []*Patch
	Name() string
}
