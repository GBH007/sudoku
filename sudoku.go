package main

import (
	"bytes"
	"strconv"
)

type Sudoku struct {
	field [9][9]int
}

func (su *Sudoku) GetHashStr() string {
	return su.print("", "")
}
func (su *Sudoku) print(sep, end string) string {
	buff := new(bytes.Buffer)
	for i := 0; i < 9; i++ {
		if i != 0 {
			buff.WriteString(end)
		}
		for j := 0; j < 9; j++ {
			if j != 0 {
				buff.WriteString(sep)
			}
			buff.WriteString(strconv.Itoa(su.field[i][j]))
		}
	}
	return buff.String()
}
func (su *Sudoku) LoadFromHashStr(s string) {
	for i := 0; i < 9; i++ {
		for j := 0; j < 9; j++ {
			n := int(s[i*9+j]) - 48
			su.field[i][j] = n
		}
	}
}
func (su *Sudoku) String() string {
	return su.print(" ", "\n")
}
