func test_value(input: felt, res1: felt, res2: felt, res3: felt, res4: felt) -> (res: felt) {
    alloc_locals;

    let value = input;

    if (value == 67) {
        return (res=res4);
    }

    if (value == 71) {
        return (res=res2);
    }

    if (value == 84) {
        return (res=res1);
    }

    if (value == 65) {
        return (res=res3);
    }
    return (res=0);
}

func main() {
    test_value(0, 1498, 997, 2753, 6301);
    let result1 = [ap - 1];
    %{ print(f"{ids.result1=}") %}

    test_value(67, 1498, 997, 2753, 6301);
    let result1 = [ap - 1];
    %{ print(f"{ids.result1=}") %}

    test_value(71, 1498, 997, 2753, 6301);
    let result1 = [ap - 1];
    %{ print(f"{ids.result1=}") %}

    test_value(84, 1498, 997, 2753, 6301);
    let result1 = [ap - 1];
    %{ print(f"{ids.result1=}") %}

    test_value(65, 1498, 997, 2753, 6301);
    let result1 = [ap - 1];
    %{ print(f"{ids.result1=}") %}
    return ();
}
