const Card = ({car}) => {
    let {brand, price, model, year, color} = car    
    return (
    <div className="shadow-md p-5 flex flex-col">
        <div className="font-extrabold text-center border-b-2">{brand} {model}</div>
        <div>Year: {year}</div>
        <div>Price: <span className="font-semibold text-orange-600">{price}</span></div>
        <div>Color: {color}</div>
    </div>
  )
}
export default Card