package main
import "fmt"

func main(){
	array := []int{1,2,3,4,5,8,2,9}

	i := 0
	j := len(array) - 1

	for i < j {
		array[i], array[j] = array[j], array[i]
        
        i++
        j--
	}

	fmt.Println(array)
}