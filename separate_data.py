''' this script divides the data into training, testing and validation data. ''' 

if __name__ == '__main__': 
    f = open('full_data_final.csv')
    trf = open('training_data.csv', 'w')
    tsf = open('testing_data.csv', 'w')
    vf = open('validation_data.csv', 'w')
    count = 0

    headers = f.readline()
    line = f.readline()
    while line: 
        if count % 10 == 8: 
            tsf.write(line)
        elif count % 10 == 9: 
            vf.write(line)
        else: 
            trf.write(line)
        line = f.readline()
        count += 1

    f.close()
    trf.close()
    tsf.close()
    vf.close()