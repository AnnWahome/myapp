import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom'
import styled from 'styled-components'
import { Link } from 'react-router-dom'

function SearchedVulnerable() {

    const[searchedRecipes, setSearchedRecipes] = useState([])
    let params = useParams()

    const fetchSearched= async(name) =>{
        try{
            const res = await fetch(
              `/api/recipes/search?query=${encodeURIComponent(name)}`
            )
            const recipes = await res.json()
            setSearchedRecipes(recipes || [])
        }catch(err){
            setSearchedRecipes([])
        }
    }

    useEffect(()=>{
        fetchSearched(params.search)
    },[params.search])

  return (
    <Grid>
        
        <SearchBanner
            dangerouslySetInnerHTML={{ __html: `Results for: ${params.search}` }}
        />

        {searchedRecipes && searchedRecipes.map((item) =>{
            return(
                <Card key={item.id}>
                    <Link to={'/recipe/'+item.id}>
                        <img src={item.image}  alt={item.title}/>
                        
                        <h4 dangerouslySetInnerHTML={{ __html: item.title }} />
                    </Link>
                </Card>
            )
        })}
    </Grid>
  )
}

const SearchBanner = styled.div`
    font-size: 1.2rem;
    margin-bottom: 1rem;
`

const Grid = styled.div`
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr));
    grid-gap: 3rem;
`

const Card = styled.div`
    img{
        width: 100%;
        border-radius: 2rem;
    }
    a{
        text-decoration: none;
    }
    h4{
        text-align: center;
        padding: 1rem;
    }
`

export default SearchedVulnerable