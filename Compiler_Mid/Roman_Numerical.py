# Roman Numeral CFG Generator (1–3999)

def numerals():
    """Generate all valid Roman numerals from 1 to 3999 using CFG rules."""
    result = []
    for th in thousands():
        for h in hundreds():
            for t in tens():
                for o in ones():
                    numeral = th + h + t + o
                    if numeral:   # exclude empty string
                        result.append(numeral)
    return result


def thousands():
    return ["", "M", "MM", "MMM"]


def hundreds():
    return [
        "", "C", "CC", "CCC",
        "CD", "D", "DC", "DCC", "DCCC", "CM"
    ]


def tens():
    return [
        "", "X", "XX", "XXX",
        "XL", "L", "LX", "LXX", "LXXX", "XC"
    ]


def ones():
    return [
        "", "I", "II", "III",
        "IV", "V", "VI", "VII", "VIII", "IX"
    ]


if __name__ == "__main__":
    romans = numerals()
    print(f"Total Roman numerals generated: {len(romans)}")
    print("First 20 examples:", romans[:20])
    print("Last 10 examples:", romans[-10:])
