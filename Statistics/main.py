from Statistics import Statistics

def main():
    st_LUT = Statistics("timesLUT.txt")
    #print(st_LUT.limit_five())
    st_LUT.plot_LUT_graph("Primes per Time using Look Up Table (LUT)", "primesXtimeLUT.png")
    x_lut, y_lut = st_LUT.return_xy()

    #st_NPprime = Statistics("timesNextprevprime.txt", std=True)
    #print(st_NPprime.limit_five())
    #st_NPprime.plot_std_graph("Primes per Time using Prev and Next (Sympy)", 'primesXtimePrevNext.png')
    #x_np, y_np = st_NPprime.return_xy()


    #st_Isprime = Statistics("timesIsprime.txt", std=True)
    #st_Isprime.plot_std_graph("Primes per Time using IsPrime (Sympy)", 'primesXtimeIsPrime.png')
    #x_is, y_is = st_Isprime.return_xy()

    #Statistics.plot_all(x_lut, y_lut, "LUT", x_np, y_np, "Next, Prev (Sympy)", x_is, y_is, "IsPrime (Sympy)")


if __name__ == '__main__':
    main()