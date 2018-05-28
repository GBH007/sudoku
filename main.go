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
	file, _ := os.Create("log.log")
	log.SetOutput(file)
	c := &data.Controller{}
	//c.Load("000040700031500006600037090000093025000000000950680000080310009400008630003060000")
	c.Load("800006700026090000094715020100004067007903200250100004080579140000040350001600009")
	c.GetHashStr()
	slr := solver.Solver{}
	slr.AddStrategy(&strategy.MaxCoAN{})
	slr.Init(c)
	slr.Solve(c)
	fmt.Println("----------------------")
	fmt.Println(c.GetCountNumber()[0])
	fmt.Println(c)
	fmt.Println(slr.GetStepsCount())
	fmt.Println(c.GetHashStr() == "815426793726398415394715628139284567467953281258167934683579142972841356541632879")
}
