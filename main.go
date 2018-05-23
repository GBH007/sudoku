package main

import (
	"fmt"
	"log"
	"os"
	"sudoku/data"
	"sudoku/solver"
	"sudoku/strategy"
)

func main() {
	//p := new(strategy.Patch)
	file, _ := os.Create("log.log")
	log.SetOutput(file)
	c := data.NewSudokuDataController(data.Sudoku{})
	c.Load("000040700031500006600037090000093025000000000950680000080310009400008630003060000")
	//c.Load("000000000000000000000000000000000000000000000000000000000000000000000000000000000")
	slr := solver.Solver{}
	slr.AddStrategy(&strategy.MaxCoAN{})
	slr.AddStrategy(&strategy.MinCoRPFN{})
	slr.AddStrategy(&strategy.MinSoNitC{})
	//slr.Solve(c)
	///*
	slr.Init(c)
	fmt.Println(c.GetCountNumber()[0])
	fmt.Println(c) //*
	for i := 0; i < 600; i++ {
		fmt.Println(i, c.GetCountNumber()[0])
		if c.GetCountNumber()[0] == 0 {
			break
		}
		slr.Step()
	} //*/
	//slr.Step(c)
	//fmt.Println("----------------------")
	//slr.Step(c)
	fmt.Println("----------------------")
	fmt.Println(c.GetCountNumber()[0])
	fmt.Println(c)
}
