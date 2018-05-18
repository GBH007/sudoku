package strategy

func getMaxElementIndexFromStart(l []int, start int) int {
	ind := start
	element := 0
	for i := start; i < len(l); i++ {
		if l[i] < 9 && l[i] > element {
			element = l[i]
			ind = i
		}
	}
	return ind
}
