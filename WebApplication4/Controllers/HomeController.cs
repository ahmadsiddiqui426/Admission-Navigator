using ConsoleApp1.Data;
using Microsoft.AspNetCore.Mvc;
using System.Linq;

public class HomeController : Controller
{
    private readonly UniContext _context;

    public HomeController(UniContext context)
    {
        _context = context;
    }

    public IActionResult Index()
    {
        var fields = _context.Fields.ToList();
        // Count the number of fields and store it in ViewBag
        ViewBag.FieldCount = _context.Fields.Count();
        return View(fields);
    }

    public IActionResult FieldDetails(int id)
    {
        // Fetch universities related to the field with the provided ID
        var universities = _context.Universities
                                   .Where(u => u.FieldUniversity.Any(fu => fu.FID == id))
                                   .ToList();

        // Return a view, passing the universities as the model
        return View(universities);
    }

    // Other actions...
}