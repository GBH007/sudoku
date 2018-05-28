package main

import (
	"sudoku/data"
	"sudoku/solver"
	"sudoku/strategy"
	"testing"
)

func TestSolving(t *testing.T) {
	c := &data.Controller{}
	c.Load("800006700026090000094715020100004067007903200250100004080579140000040350001600009")
	slr := solver.Solver{}
	slr.AddStrategy(&strategy.MaxCoAN{})
	slr.Solve(c)
	if !(c.GetHashStr() == "815426793726398415394715628139284567467953281258167934683579142972841356541632879") {
		t.Fatal("некорректный ответ")
	}
}
