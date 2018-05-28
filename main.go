package main

import (
	"fmt"
	"sudoku/data"
	"sudoku/solver"
	"sudoku/strategy"
)

func main() {
	c := &data.Controller{}
	c.Load("000040700031500006600037090000093025000000000950680000080310009400008630003060000")
	slr := solver.Solver{}
	slr.AddStrategy(&strategy.MaxCoAN{})
	slr.Solve(c)
	fmt.Println("----------------------")
	fmt.Println(c.GetCountNumber()[0])
	fmt.Println(c)
	fmt.Println(slr.GetStepsCount())
}
