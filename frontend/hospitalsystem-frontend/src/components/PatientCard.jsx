function PatientCard({name,age,gender}){
    return(
        <div>
            <h3>{name}</h3>
            <p>{age}</p>
            <p>{gender}</p>
        </div>
    );
}
export default PatientCard;